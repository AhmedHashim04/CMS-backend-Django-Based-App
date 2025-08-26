# Company Management System – Back End

--screen

## Description
A back-end Company Management System built with role-based access control, RESTful APIs, and an employee performance review workflow. Supports CRUD operations for companies, departments, employees, and projects. Designed to ensure secure data handling and efficient workflow management.

---

## Table of Contents
- [Features](#features)
- [Data Models](#data-models)
- [Employee Performance Review Workflow](#employee-performance-review-workflow)
- [Security & Permissions](#security--permissions)
- [RESTful API](#restful-api)
- [Testing](#testing)
- [Logging (Bonus)](#logging-bonus)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Checklist](#checklist)
- [License](#license)

---

## Features
- CRUD operations for Companies, Departments, Employees, and Projects
- Employee performance review workflow with approval stages
- Role-based access control (Admin, Manager, Employee)
- Secure authentication & authorization
- RESTful API for all entities
- Optional: Logging for error tracking and application behavior

---

## Data Models

### User Accounts
- Username
- Email Address (Login ID)
- Role

### Company
- Company Name
- Number of Departments (auto-calculated)
- Number of Employees (auto-calculated)
- Number of Projects (auto-calculated)

### Department
- Company (Select)
- Department Name
- Number of Employees (auto-calculated)
- Number of Projects (auto-calculated)

### Employee
- Company (Select)
- Department (Select)
- Employee Name
- Email Address
- Mobile Number
- Address
- Designation
- Hired On (optional)
- Days Employed (auto-calculated)

### Project (Bonus)
- Company (Select)
- Department (Select)
- Project Name
- Description
- Start Date
- End Date
- Assigned Employees (Multi-Select)

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
- Under Approval → Review Approved
- Under Approval → Review Rejected
- Review Rejected → Feedback Provided

---

## Security & Permissions
- Role-based access control: Admin, Manager, Employee
- Secure authentication & authorization (Sessions, Tokens, etc.)
- Different roles have different levels of access

---

## RESTful API
**Company**
- GET: Retrieve single company
- GET: List all companies

**Department**
- GET: Retrieve single department
- GET: List all departments

**Employee**
- POST: Create new employee
- GET: Retrieve single employee
- GET: List all employees
- PATCH: Update employee
- DELETE: Delete employee

**Project (Bonus)**
- POST: Create new project
- GET: Retrieve single project
- GET: List all projects
- PATCH: Update project
- DELETE: Delete project

**Notes:**
- API follows RESTful conventions
- Handles data securely
- API documentation provided

---

## Testing
- Unit tests for individual components/functions
- Integration tests for full application workflow

---

## Logging (Bonus)
- Logging implemented for application behavior and error tracking
- Logs do not expose sensitive information

---

## Setup & Installation

```bash
# Clone repository
git clone https://github.com/AhmedHashim04/CMS-backend-Django-Based-App.git

# Navigate into the project directory
cd CMS-backend-Django-Based-App

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
