# Backend Documentation

This directory contains the Flask-based REST API for the Hospital Management System.

## Project Structure

- **`app.py`**: The entry point of the application. It uses the **Application Factory Pattern** (`create_app`) to initialize the Flask app, register extensions (database, JWT, caching), and register blueprints (routes).
- **`config.py`**: Contains configuration classes (e.g., `Config`) for setting up database URIs, secret keys, and Redis URLs.
- **`extensions.py`**: Initializes Flask extensions (SQLAlchemy, JWTManager, Cache, Celery) separately to avoid circular import issues.
- **`models.py`**: Defines the database schema using SQLAlchemy ORM. Classes here represent tables in the SQLite database (e.g., `User`, `Doctor`, `Appointment`).
- **`tasks.py`**: Defines background jobs to be run by Celery (e.g., sending emails, generating reports).
- **`celery_worker.py`**: A separate entry point to start the Celery worker process.

## Routes (Blueprints)

The API is divided into modules called "Blueprints" located in the `routes/` folder:

- **`auth.py`**: Handles User Authentication (Login, Register, Get Current User).
- **`admin.py`**: Admin-specific functionalities (Manage Doctors, View Stats).
- **`doctor.py`**: Doctor-specific functionalities (View Appointments, Complete Consultations).
- **`patient.py`**: Patient-specific functionalities (Book Appointments, View History).

## Key Concepts

- **JWT (JSON Web Tokens)**: Used for secure authentication. When a user logs in, they receive a token. This token must be sent in the `Authorization` header of subsequent requests.
- **SQLAlchemy**: An ORM (Object Relational Mapper) that allows us to interact with the database using Python classes instead of writing raw SQL queries.
- **Celery**: A distributed task queue. We use it to offload time-consuming tasks (like generating reports) so the API remains fast and responsive.
