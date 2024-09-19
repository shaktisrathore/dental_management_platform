# Dental Clinic Management System

## Overview
This project is a comprehensive Dental Clinic Management System developed using Django and Django REST Framework. It provides functionalities to manage clinics, doctors, patients, and appointments through both a web interface and RESTful APIs.

## Demo

Check out our YouTube demo to see the Dental Clinic Management System in action:

[![Dental Clinic Management System Demo](https://img.youtube.com/vi/dxmbzaPectU/0.jpg)](https://youtu.be/dxmbzaPectU?si=eBxUO0hICSF1Yp6k)

[Watch the demo video](https://youtu.be/dxmbzaPectU?si=eBxUO0hICSF1Yp6k)

This video provides an overview of the key features and functionalities of our Dental Clinic Management System.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Running the Platform](#running-the-platform)
5. [Using Key Features and REST APIs](#using-key-features-and-rest-apis)
6. [Unit Tests](#unit-tests)
7. [Configurations](#configurations)
8. [Environment Variables](#environment-variables)
9. [Troubleshooting](#troubleshooting)

## Features
- **Clinic Management**: Add, edit, and view clinic information.
- **Doctor Management**: Manage doctor profiles, specialties, and clinic affiliations.
- **Patient Management**: Handle patient records and medical history.
- **Appointment Scheduling**: Schedule and manage patient appointments with doctors.
- **User Authentication**: Secure login and registration system.
- **RESTful API**: Full API support for integration with other systems.
- **CORS Support**: Cross-Origin Resource Sharing for API access from different domains.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- PostgreSQL (optional, SQLite is used by default for development)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/shaktisrathore/dental_management_platform.git
cd dental_management_platform
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage project dependencies.
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory of the project (dental_manage_v1/) and add the following variables:

```bash
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Replace `your_secret_key_here` with a secure random string, and update the `DATABASE_URL` with your PostgreSQL credentials.

### 5. Database Setup (PostgreSQL)
By default, the project uses SQLite. To use PostgreSQL:

1. Install PostgreSQL on your system if not already installed.
2. Create a new PostgreSQL database for the project.
3. Update the DATABASE CREDEBTIALS in your `.env` file with your PostgreSQL credentials.

### 5. Apply Migrations
Set up the database schema by applying migrations.
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)
Create a superuser to access the Django admin interface.
```bash
python manage.py createsuperuser
```

## Running the Platform
1. Start the Development Server
```bash
python manage.py runserver
```
The platform will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Using Key Features and REST APIs

### Key Features
- **Clinics**: Manage clinic information.
- **Doctors**: Manage doctor profiles and their specialties.
- **Patients**: Manage patient records and appointments.

### REST APIs
- **Add Clinic**
  - **Endpoint**: `POST /api/clinics/add/`
  - **Description**: Add a new clinic.

- **Add Doctor**
  - **Endpoint**: `POST /api/doctors/add/`
  - **Description**: Add a new doctor.

- **Add Patient**
  - **Endpoint**: `POST /api/patients/add/`
  - **Description**: Add a new patient.

- **Get Clinic Info By ID**
  - **Endpoint**: `GET /api/clinics/get/<int:pk>/`
  - **Description**: Get clinic information by ID.

For detailed API documentation, refer to the Django REST Framework browsable API interface when the server is running.

## Unit Tests

This project includes a comprehensive suite of unit tests to ensure the reliability and correctness of its components. The tests cover various aspects of the system, including models, views, and API endpoints.

### Running the Tests

To run the unit tests, use the following command:

```bash
python manage.py test
```

This will discover and run all the tests in the project.

### Test Coverage

The tests cover critical functionalities such as:

- Model creation and validation
- API endpoint responses
- Form submissions
- User authentication and authorization

## Configurations
Key configuration options are available in `dental_management_platform/settings.py`, including database settings, installed apps, and middleware.

## Environment Variables
The `.env` file contains important configuration settings:
- `DJANGO_SECRET_KEY`: Secret key for Django's cryptographic signing.
- `DJANGO_DEBUG`: Set to 'True' for development, 'False' for production.
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `CORS_ALLOWED_ORIGINS`: Allowed origins for CORS (in development mode, all origins are allowed).
- `DB_NAME`: Name of the database.
- `DB_USER`: Database user.
- `DB_PASSWORD`: Database password.
- `DB_HOST`: Database host.
- `DB_PORT`: Database port. 

## Troubleshooting
- **Database Issues**: Ensure migrations are applied.
- **Static Files Not Loading**: Run `python manage.py collectstatic`.
- **API Access Issues**: Check CORS settings in `settings.py`.