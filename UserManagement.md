# Project Overview: UH Form Management & RBAC System

## Overview

This project is a **Django-based web application** designed for managing users, roles, and a **form submission + approval workflow** system for **University of Houston (UH) students and staff**. It supports:

- **Role-Based Access Control (RBAC)**
- **Microsoft 365 authentication**
- **Custom form handling and signing**
- **Admin user management tools**
- **Live digital signature capture**
- **Dockerized deployment with Azure hosting**

---

## System Stack

| Layer         | Technology Used                                  |
|--------------|---------------------------------------------------|
| Backend       | Django (Python)                                  |
| Frontend      | HTML, CSS, JavaScript                            |
| Authentication| Microsoft 365 OAuth, traditional login           |
| Database      | PostgreSQL                                       |
| Hosting       | Azure Web Service                                |
| Containerization | Docker                                        |

---

## Key Features

- **Microsoft & Local Login**: Supports Microsoft 365 single sign-on (SSO) and fallback password-based login.
- **Role-Based Access Control**: Admins, staff, and students have different access and permissions.
- **Form Workflow**:
  - Users can submit **Payroll** or **Reimbursement** forms.
  - Forms go through approval workflow with status tracking.
  - Admins can view, approve/reject, or live-sign forms.
- **Live Signature Support**: Forms support digital signatures using an HTML5 `<canvas>` + base64 backend storage.
- **PDF Generation**: Submitted forms are converted to signed PDFs for record keeping.
- **Admin Panel**: Built-in panel for managing users, roles, and viewing submission activity.

---

## Database Model Summary

### `user_accs` (custom user model)
- Email-based authentication

### `roles`
- Role definitions (admin, user)
### `permission`
- Assigns permission details to roles
- One-to-many: one role can have many permissions

---

### `PayrollAssignment`
Handles detailed payroll-related form submissions including:
- User and employee info
- Multiple position data (for hire/rehire/changes)
- Change types: FTE, pay rate, budget, termination, etc.
- Admin message and digital signature
- Status: Draft, Pending, Approved, Rejected, Cancelled
- Only one pending payroll form per user is allowed

---

### `ReimbursementRequest`
Handles travel/expense reimbursements:
- User and employee info
- Reimbursement details and cost centers
- Admin and user signature fields 
- Status: Draft, Pending, Approved, Rejected, Cancelled
- Enforces one pending reimbursement per user

---

## Authentication Flow

- **Microsoft Login**:
  - Users authenticate via Microsoft OAuth
  - Session tokens are stored securely
- **Custom Login**:
  - Passwords are hashed using Django's `make_password`
  - Validated using Django’s authentication backend

---

## Deployment

- Dockerized for consistency and scalability
- Deployed on Azure Web App with PostgreSQL backend
- Static files served via Django's staticfiles config

---

## Admin Use Case

1. Log in via Microsoft SSO or admin credentials
2. View and manage user accounts (delete/ban/create)
3. Monitor form activity (pending/approved/rejected)
4. Sign and approve forms live with signature pad
5. View or download PDF versions of submitted forms

---

##  Team members
Tran Minh Nhat Pham (NhatPham123tm): 
  + Authentication feature for both login method
  + RBAC for admin and basic user
  + Reset password feature
  + Display statistics + chart in admin front-end
  + Home landing page

Son nguyen:
  + created the login page html css
  + created the user profile html css
  + created the edit profile for user javascript
  + Assisted on the other page html css

Ricardo Jesus Prieto (ricarpr):
  + Created admin page with corresponding CSS
  + CRUD utilities for admin in frontend
  + Assisted in User page

Tien Phu Tran (TienPhuTran):
  + Created and deployed database model (api/models.py - add models)
  + Adjusted and responsible Web App Backend connections (API + authentication folders)
  + Connect API to PostgreSQL (api/serilizers.py + api/views.py + api/urls.py)
  + Create and responsible for the register page (authentication/views.py + authentication/urls.py + templates/register.html - add frontend input (user) to database)
  + Created Suspend page redirect to inactive/ban users (authentication/views.py + authentication/urls.py + templates/suspend.html - delete all user local storage and direct to suspend page)
  + Online Deployment (Copy repository and set up the connections in another repository for online deployment)
