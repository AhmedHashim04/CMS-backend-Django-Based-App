import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from company.models import Company, Department, Project
from user.models import Employee, User
from faker import Faker
from django.db.models.signals import post_save
from user.signals import create_employee
from django.dispatch import receiver

fake = Faker()

@pytest.fixture(autouse=True)
def clear_db(db):
    User.objects.all().delete()
    Employee.objects.all().delete()
    Company.objects.all().delete()
    Department.objects.all().delete()
    Project.objects.all().delete()

@pytest.fixture(autouse=True)
def disable_employee_signal():
    post_save.disconnect(create_employee, sender=User)
    yield
    post_save.connect(create_employee, sender=User)


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
    username="testuser",
    email=fake.unique.email(),
    password="password123",
    role="Admin")

@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def company(db):
    return Company.objects.create(name="Test Company", slug="test-company")

@pytest.fixture
def department(db, company):
    return Department.objects.create(name="HR", slug="hr", company=company)

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="emp1",
        email="emp1@example.com",
        password="pass1234",
        role="employee"
    )

@pytest.fixture
def employee(db, user, company, department):
    return Employee.objects.create(
        user=user,
        name="Employee One",
        company=company,
        department=department,
        slug="employee-one"
    )

@pytest.fixture
def project(db, company, department):
    return Project.objects.create(
        name="Project X",
        slug="project-x",
        company=company,
        department=department,
        description="Test project",
        start_date="2025-01-01",
        end_date="2025-12-31",
    )

# --- Company Tests ---
@pytest.mark.django_db
def test_list_companies(auth_client, company):
    url = reverse('company-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert company.name in str(response.data)

@pytest.mark.django_db
def test_retrieve_company(auth_client, company):
    url = reverse('company-detail', args=[company.slug])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == company.name

# --- Department Tests ---
@pytest.mark.django_db
def test_list_departments(auth_client, department):
    url = reverse('department-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert department.name in str(response.data)

@pytest.mark.django_db
def test_retrieve_department(auth_client, department):
    url = reverse('department-detail', args=[department.slug])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == department.name

# --- Project Tests ---
@pytest.mark.django_db
def test_create_project(auth_client, company, department):
    url = reverse('project-list')
    data = {
        "name": "Project Y",
        "slug": "project-y",
        "company": company.slug,
        "department": department.slug,
        "description": "Another project",
        "start_date": "2025-02-01",
        "end_date": "2025-05-01"
    }
    response = auth_client.post(url, data)
    print(response.status_code)

    assert response.status_code == 201
    assert response.data['name'] == "Project Y"

@pytest.mark.django_db
def test_list_projects(auth_client, project):
    url = reverse('project-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert project.name in str(response.data)

@pytest.mark.django_db
def test_retrieve_project(auth_client, project):
    url = reverse('project-detail', args=[project.slug])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == project.name

@pytest.mark.django_db
def test_update_project(auth_client, project):
    url = reverse('project-detail', args=[project.slug])
    data = {"description": "Updated description"}
    response = auth_client.patch(url, data)
    assert response.status_code == 200
    assert response.data['description'] == "Updated description"

@pytest.mark.django_db
def test_delete_project(auth_client, project):
    url = reverse('project-detail', args=[project.slug])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Project.objects.filter(slug=project.slug).exists()

# --- Employee Tests ---
@pytest.mark.django_db
def test_create_employee(auth_client, company, department):
    user = User.objects.create_user(
        username="emp4",
        email="emp4@example.com",
        password="pass1234",
        role="employee"
    )
    url = reverse('employee-list')
    data = {
        "user": user.id,
        "name": "Employee Two",

        "mobile": "1234567890",
        "address": "123 Main St",
        "position": "Developer",
        "slug": "employee-two"
    }
    response = auth_client.post(url, data)
    print(response.data)
    assert response.status_code == 201
    assert response.data['name'] == "Employee Two"

@pytest.mark.django_db
def test_list_employees(auth_client):
    url = reverse('employee-list')
    response = auth_client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_retrieve_employee(auth_client, employee):
    url = reverse('employee-detail', args=[employee.slug])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == employee.name

@pytest.mark.django_db
def test_update_employee(auth_client, employee):
    url = reverse('employee-detail', args=[employee.slug])
    data = {"name": "Employee 1 Updated"}
    response = auth_client.patch(url, data)
    assert response.status_code == 200
    assert response.data['name'] == "Employee 1 Updated"

@pytest.mark.django_db
def test_delete_employee(auth_client, employee):
    url = reverse('employee-detail', args=[employee.slug])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Employee.objects.filter(slug=employee.slug).exists()

# --- Integration Test ---

@pytest.mark.django_db
def test_create_project_and_assign_employee(auth_client, company, department, employee):
    project_data = {
        "name": "Integration Project",
        "slug": "integration-project",
        "company": company.slug,
        "department": department.slug,
        "description": "Integration test project",
        "start_date": "2025-03-01",
        "assigned_employees": [employee.id],
        "end_date": "2025-06-01"
    }
    project_response = auth_client.post(reverse('project-list'), project_data)
    assert project_response.status_code == 201
    project_slug = project_response.data['slug']

    project = Project.objects.get(slug=project_slug)
    project.assigned_employees.add(employee)
    project.save()

    response = auth_client.get(reverse('project-detail', args=[project.slug]))
    assert response.status_code == 200
    assert employee.name in [emp for emp in response.data['assigned_employees']]