# Office Management System

## Project Description
This is a Django-based Office Management System designed to manage students, staff, attendance, internal marks, fees, and notifications. It supports different user roles including students, teaching staff, non-teaching staff, and administrators, each with specific access and functionalities.

## Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd student_management
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # Assuming a requirements.txt exists, if not, install django
    ```
4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be accessible at `http://127.0.0.1:8000/`.

## User Roles and Permissions

The system defines the following user roles with distinct access levels:

*   **Anonymous User**: Can only access the login page.
*   **Student**: Can view their own dashboard, details, and notifications.
*   **Teaching Staff**: Can view students under their charge, manage attendance, and upload internal marks.
*   **Non-Teaching Staff**: Can view all students, register new students, update fee statuses, register new staff, and access admin reports.
*   **Superuser**: Has full access to the Django admin panel and all functionalities.

## Available Endpoints

### General Endpoints

| URL Pattern             | View Function           | Description                                     | Required Permissions |
| :---------------------- | :---------------------- | :---------------------------------------------- | :------------------- |
| `/`                     | `office.views.home`     | Home page of the application.                   | All Users            |
| `/login/`               | `office.views.CustomLoginView` | User login page.                                | Anonymous Users      |
| `/logout/`              | `django.contrib.auth.views.LogoutView` | User logout.                                    | Authenticated Users  |
| `/admin/`               | `django.contrib.admin.site.urls` | Django administration panel.                    | Superuser            |

### Student Endpoints

| URL Pattern             | View Function           | Description                                     | Required Permissions |
| :---------------------- | :---------------------- | :---------------------------------------------- | :------------------- |
| `/office/student/dashboard/` | `office.views.student_dashboard` | Student's personal dashboard.                   | Authenticated Student |
| `/office/student/detail/` | `office.views.student_detail` | View current student's details.                 | Authenticated Student |
| `/office/student/detail/<int:student_id>/` | `office.views.student_detail` | View details of a specific student.             | Authenticated Student (if `student_id` matches current user) or Staff |
| `/office/notifications/` | `office.views.notification_list` | List of all notifications.                      | Authenticated Users  |

### Teaching Staff Endpoints

| URL Pattern             | View Function           | Description                                     | Required Permissions |
| :---------------------- | :---------------------- | :---------------------------------------------- | :------------------- |
| `/office/staff/dashboard/` | `office.views.office_staff_dashboard` | Staff dashboard (accessible to all staff types). | Authenticated Staff  |
| `/office/staff/teaching/` | `office.views.teaching_staff_view` | View students under the teaching staff's charge. | Teaching Staff       |
| `/office/staff/manage-attendance/` | `office.views.manage_attendance` | Manage attendance for students.                 | Teaching Staff       |
| `/office/staff/upload-marks/` | `office.views.upload_internal_marks` | Upload internal marks for students.             | Teaching Staff       |

### Non-Teaching Staff Endpoints

| URL Pattern             | View Function           | Description                                     | Required Permissions |
| :---------------------- | :---------------------- | :---------------------------------------------- | :------------------- |
| `/office/staff/dashboard/` | `office.views.office_staff_dashboard` | Staff dashboard (accessible to all staff types). | Authenticated Staff  |
| `/office/staff/non-teaching/` | `office.views.non_teaching_staff_view` | View all students.                              | Non-Teaching Staff   |
| `/office/staff/register-student/` | `office.views.register_student` | Register a new student.                         | Non-Teaching Staff   |
| `/office/staff/register/` | `office.views.register_staff` | Register a new staff member.                    | Non-Teaching Staff   |
| `/office/student/<int:student_id>/update-fee/` | `office.views.update_fee_status` | Update fee status for a specific student.       | Non-Teaching Staff   |
| `/office/admin/reports/` | `office.views.admin_reports_view` | Access administrative reports.                  | Non-Teaching Staff   |