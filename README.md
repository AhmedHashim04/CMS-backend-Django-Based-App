# Company Management System – Back End

Checklist
- ✅ CRUD for all entities
- ✅ Role-based access control
- ✅ JWT authentication
- ✅ Employee performance review workflow
- ✅ RESTful API
- ✅ API documentation
- ✅ Logging
- ✅ Unit & integration tests

![Company Management System](image.png)
![ERD](MyModels.png)
![Tests](image-1.png)
![looging](image-2.png)

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



# Setup Guide

This guide explains how to set up and run a Django project on **Windows** and **Linux** step by step.

---

## 📌 Prerequisites
Make sure you have the following installed before starting:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [pip](https://pip.pypa.io/en/stable/installation/) (comes with Python)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

---

## ⚙️ 1. Create Virtual Environment

### ▶ On **Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### ▶ On **Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🚀 2. Clone the Project
Clone the repository from GitHub:

```bash
git clone https://github.com/AhmedHashim04/CMS-backend-Django-Based-App.git
mv CMS-backend-Django-Based-App venv
cd venv
mv CMS-backend-Django-Based-App src
cd src

```

---

## 📦 3. Install Dependencies
Install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🛠️ 4. Database Setup

### ▶ Default (SQLite)
the project uses **SQLite**, no extra setup is needed.



---

## 📂 6. Apply Migrations
Run database migrations:

```bash
python manage.py migrate
```

---

## 👤 7. Create Superuser
```bash
python manage.py createsuperuser
```

---

## 🌐 8. Run Development Server
```bash
python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000/api/docs/
```
and u can test all views
---

## 🧪 9. Run Tests
```bash
pytest

```

---

## 🗂️ 10. Static & Media Files (Optional)
Collect static files:
```bash
python manage.py collectstatic
```

---

## 🔧 11. Extra (Linux Only)
If you face permission issues:
```bash
chmod +x manage.py
```


---

## ✅ Summary
1. Clone project  
2. Create virtual environment  
3. Install dependencies  
4. Setup database & env variables  
5. Run migrations  
6. Create superuser  
7. Start server 🚀  

---

### 📄 License
No License.