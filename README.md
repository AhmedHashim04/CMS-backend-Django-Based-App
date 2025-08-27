# Company Management System – Back End

![Company Management System](image.png)

## Description

A robust back-end Company Management System built with Django and Django REST Framework. The system features role-based access control, secure authentication, and a comprehensive employee performance review workflow. It supports CRUD operations for companies, departments, employees, and projects, with RESTful APIs and optional logging for error tracking and application behavior.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Data Models](#data-models)
- [Employee Performance Review Workflow](#employee-performance-review-workflow)
- [Security & Permissions](#security--permissions)
- [RESTful API](#restful-api)
- [Testing](#testing)
- [Logging](#logging)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Checklist](#checklist)
- [License](#license)

---

## Features

- CRUD operations for Companies, Departments, Employees, and Projects
- Employee performance review workflow with approval stages
- Role-based access control (Admin, Manager, Employee)
- Secure authentication & authorization (JWT)
- RESTful API for all entities
- API documentation (Swagger & ReDoc)
- Logging for error tracking and application behavior

---

## Architecture

- **Django**: Web framework for rapid development
- **Django REST Framework**: For building RESTful APIs
- **JWT Authentication**: Secure token-based authentication
- **Modular Apps**: `user`, `company`, `performance_review`
- **SQLite**: Default database (can be swapped for PostgreSQL/MySQL)
- **Logging**: Configured for both application and error logs

---

## Data Models

### User Accounts
- Username
- Email Address (Login ID)
- Role (Manager, Employee)

### Company
- Name
- Number of Departments (auto-calculated)
- Number of Employees (auto-calculated)
- Number of Projects (auto-calculated)

### Department
- Company (ForeignKey)
- Name
- Number of Employees (auto-calculated)
- Number of Projects (auto-calculated)

### Employee
- Company (ForeignKey)
- Department (ForeignKey)
- Name
- Email Address
- Mobile Number
- Address
- Designation
- Hired On (optional)
- Days Employed (auto-calculated)

### Project
- Company (ForeignKey)
- Department (ForeignKey)
- Name
- Description
- Start Date
- End Date
- Assigned Employees (Many-to-Many)

### Performance Review
- Employee (ForeignKey)
- Stage (workflow status)
- Scheduled Date
- Feedback
- Reviewed By
- Approved By
- Created/Updated timestamps

---

## Employee Performance Review Workflow

**Stages:**
1. Pending Review
2. Review Scheduled
3. Feedback Provided
4. Under Approval
5. Review Approved
6. Review Rejected

**Transitions:**
- Pending Review → Review Scheduled
- Review Scheduled → Feedback Provided
- Feedback Provided → Under Approval
- Under Approval → Review Approved / Review Rejected
- Review Rejected → Feedback Provided

---

## Security & Permissions

- Role-based access control: Admin, Manager, Employee
- JWT authentication for all endpoints
- Managers can access their department's data; employees can access their own
- Secure password storage and validation

---

## RESTful API

**Company**
- `GET /api/companies/`: List all companies
- `GET /api/companies/<slug>/`: Retrieve single company

**Department**
- `GET /api/departments/`: List all departments
- `GET /api/departments/<slug>/`: Retrieve single department

**Employee**
- `POST /api/employees/`: Create new employee
- `GET /api/employees/`: List all employees
- `GET /api/employees/<slug>/`: Retrieve single employee
- `PATCH /api/employees/<slug>/`: Update employee
- `DELETE /api/employees/<slug>/`: Delete employee

**Project**
- `POST /api/projects/`: Create new project
- `GET /api/projects/`: List all projects
- `GET /api/projects/<slug>/`: Retrieve single project
- `PATCH /api/projects/<slug>/`: Update project
- `DELETE /api/projects/<slug>/`: Delete project

**Performance Review**
- `GET /api/performance-reviews/`: List all reviews (filtered by role)
- `POST /api/performance-reviews/`: Create review
- `PATCH /api/performance-reviews/<id>/transition/`: Transition review stage

**Authentication**
- `POST /api/register/`: Register new user
- `POST /api/login/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

**Notes:**
- API follows RESTful conventions
- Handles data securely
- API documentation provided at `/api/docs/` (Swagger) and `/api/redoc/` (ReDoc)

---

## Testing

- Unit tests for models, serializers, and views
- Integration tests for full application workflow
- Run all tests with:
  ```bash
  python manage.py test
````
