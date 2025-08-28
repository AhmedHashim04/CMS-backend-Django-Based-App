import os
import django
import random
import argparse
from datetime import date, timedelta
from faker import Faker

# تهيئة Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")  # غيّر اسم المشروع هنا
django.setup()

from company.models import Company, Department, Project
from user.models import User, Employee 


fake = Faker()

def create_users(num):
    users = []
    for _ in range(num):
        email = fake.unique.email()
        user = User.objects.create_user(
            username=fake.user_name(),
            email=email,
            password="123456",
            role=random.choice([User.ROLES.ADMIN, User.ROLES.MANAGER, User.ROLES.EMPLOYEE])
        )
        users.append(user)
    return users


def create_companies(num):
    companies = []
    for _ in range(num):
        company = Company.objects.create(
            name=fake.unique.company()
        )
        companies.append(company)
    return companies


def create_departments(companies, num):
    departments = []
    for _ in range(num):
        company = random.choice(companies)
        department = Department.objects.create(
            company=company,
            name=fake.unique.bs().title()
        )
        departments.append(department)
    return departments


def create_employees(users, companies, departments):
    employees = []
    for user in users:
        company = random.choice(companies)
        department = random.choice(departments)

        employee = Employee.objects.create(
            user=user,
            company=company,
            department=department,
            name=fake.name(),
            email=user.email,
            mobile=fake.phone_number(),
            address=fake.address(),
            position=fake.job(),
            hired_on=fake.date_between(start_date="-3y", end_date="today")
        )
        employees.append(employee)
    return employees



def create_projects(companies, departments, employees, num):
    projects = []
    for _ in range(num):
        company = random.choice(companies)
        department = random.choice(departments)

        project = Project.objects.create(
            company=company,
            department=department,
            name=fake.catch_phrase(),
            description=fake.text(),
            start_date=fake.date_between(start_date="-2y", end_date="-1y"),
            end_date=fake.date_between(start_date="-1y", end_date="today"),
        )

        # ربط موظفين بالمشروع
        assigned = random.sample(employees, k=min(len(employees), random.randint(2, 5)))
        project.assigned_employees.set(assigned)
        projects.append(project)
    return projects


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed database with dummy data")
    parser.add_argument("--companies", type=int, default=5, help="Number of companies")
    parser.add_argument("--departments", type=int, default=10, help="Number of departments")
    parser.add_argument("--employees", type=int, default=30, help="Number of employees")
    parser.add_argument("--projects", type=int, default=15, help="Number of projects")

    args = parser.parse_args()

    print("Seeding database...")
    users = create_users(args.employees)
    companies = create_companies(args.companies)
    departments = create_departments(companies, args.departments)
    employees = create_employees(users, companies, departments)  # ← بدون num
    projects = create_projects(companies, departments, employees, args.projects)



    print(f"✅ Created {len(users)} users, {len(companies)} companies, {len(departments)} departments, {len(employees)} employees, {len(projects)} projects")


# python seed.py --companies 3 --departments 6 --employees 15 --projects 10
