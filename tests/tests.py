from company.views import CompanyViewSet, DepartmentViewSet, ProjectViewSet
from user.views import EmployeeViewSet


    # Task : with pytest
        # a. Include unit tests to validate individual components and functions.
        # b. Include integration tests to ensure different parts of the application work together correctly.
    
    # i. Company: from CompanyViewSet
    #     • GET: Retrieve a single company or list all companies

    # ii. Department: from DepartmentViewSet
    #     • GET: Retrieve a single department or list all departments

    # iii. Project : from ProjectViewSet
    #     • POST: Create a new project
    #     • GET: Retrieve a single project or list all projects
    #     • PATCH: Update an existing project
    #     • DELETE: Delete a project

    # iv. Employee : from EmployeeViewSet
    #     • POST: Create a new employee
    #     • GET: Retrieve a single employee or list all employees
    #     • PATCH: Update an existing employee
    #     • DELETE: Delete an employee

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from company.models import Company, Department, Project
from user.models import Employee, User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def company():
    return Company.objects.create(name="Test Company")

@pytest.fixture
def department(company):
    return Department.objects.create(name="HR", company=company)

@pytest.fixture
def user():
    return User.objects.create_user(username="emp1", email="emp1@example.com", password="pass1234", role="Employee")

@pytest.fixture
def employee(user, company, department):
    return Employee.objects.create(
        user=user,
        name="Employee One",
        email="emp1@example.com",
        company=company,
        department=department
    )

@pytest.fixture
def project(company, department):
    return Project.objects.create(
        name="Project X",
        company=company,
        department=department,
        description="Test project"
    )

# --- CompanyViewSet Tests ---

def test_list_companies(api_client, company):
    url = reverse('company-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert company.name in str(response.data)

def test_retrieve_company(api_client, company):
    url = reverse('company-detail', args=[company.slug])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == company.name

# --- DepartmentViewSet Tests ---

def test_list_departments(api_client, department):
    url = reverse('department-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert department.name in str(response.data)

def test_retrieve_department(api_client, department):
    url = reverse('department-detail', args=[department.slug])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == department.name

# --- ProjectViewSet Tests ---

def test_create_project(api_client, company, department):
    url = reverse('project-list')
    data = {
        "name": "Project Y",
        "company": company.id,
        "department": department.id,
        "description": "Another project"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == "Project Y"

def test_list_projects(api_client, project):
    url = reverse('project-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert project.name in str(response.data)

def test_retrieve_project(api_client, project):
    url = reverse('project-detail', args=[project.slug])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == project.name

def test_update_project(api_client, project):
    url = reverse('project-detail', args=[project.slug])
    data = {"description": "Updated description"}
    response = api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data['description'] == "Updated description"

def test_delete_project(api_client, project):
    url = reverse('project-detail', args=[project.slug])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Project.objects.filter(slug=project.slug).exists()

# --- EmployeeViewSet Tests ---

def test_create_employee(api_client, company, department):
    user = User.objects.create_user(username="emp2", email="emp2@example.com", password="pass1234", role="Employee")
    url = reverse('employee-list')
    data = {
        "user": user.id,
        "name": "Employee Two",
        "email": "emp2@example.com",
        "company": company.id,
        "department": department.id
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == "Employee Two"

def test_list_employees(api_client, employee):
    url = reverse('employee-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert employee.name in str(response.data)

def test_retrieve_employee(api_client, employee):
    url = reverse('employee-detail', args=[employee.slug])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == employee.name

def test_update_employee(api_client, employee):
    url = reverse('employee-detail', args=[employee.slug])
    data = {"name": "Employee 1 Updated"}
    response = api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data['name'] == "Employee 1 Updated"

def test_delete_employee(api_client, employee):
    url = reverse('employee-detail', args=[employee.slug])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Employee.objects.filter(slug=employee.slug).exists()

# --- Integration Test Example ---

def test_create_project_and_assign_employee(api_client, company, department, employee):
    # Create a project
    project_data = {
        "name": "Integration Project",
        "company": company.id,
        "department": department.id,
        "description": "Integration test project"
    }
    project_response = api_client.post(reverse('project-list'), project_data)
    assert project_response.status_code == 201
    project_id = project_response.data['id']

    # Assign employee to project (assuming M2M field 'assigned_employees')
    project = Project.objects.get(id=project_id)
    project.assigned_employees.add(employee)
    project.save()

    # Retrieve project and check employee assignment
    response = api_client.get(reverse('project-detail', args=[project.slug]))
    assert response.status_code == 200
    assert employee.name in [emp['name'] for emp in response.data['assigned_employees']]
