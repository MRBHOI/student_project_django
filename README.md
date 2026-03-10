"# Django Student Management System" 
# student_project_django
A Student Management System built using Django that allows authenticated users to manage student records with full CRUD functionality. The system includes authentication, search functionality, validation rules, admin customization, and additional features like pagination and CSV export.
# Student Management System

A Django-based Student Management System with authentication, CRUD, search, pagination, CSV export, and admin customization.

## Setup Instructions

### 1. Clone and enter the project
```bash
git clone <your-repo-url>
cd student_project
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin + delete access)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

### 7. Open in browser
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Features

- User Registration / Login / Logout
- Add, Edit, Delete Students (delete restricted to superuser)
- Search by name or course
- Pagination (5 per page)
- Export all students to CSV
- Dashboard with total count
- Django Admin with list_display, search_fields, list_filter
- Server-side validation (unique email, 10-digit phone, name without digits)
