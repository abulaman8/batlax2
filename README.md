# Hospital Management System (HMS)

A full-stack Hospital Management System built with Flask (Backend) and Vue.js (Frontend), featuring role-based access control (Admin, Doctor, Patient), appointment booking, and background job processing.

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Caching
- **Frontend:** Vue 3, Vite, Vuex, Bootstrap 5, Chart.js
- **Database:** SQLite
- **Background Jobs:** Celery, Redis
- **Caching:** Redis

## Prerequisites

- Python 3.8+
- Node.js 16+
- Redis Server (must be installed and running)

## Setup Instructions

### 1. Backend Setup

Navigate to the project root:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database (creates `instance/hms.db` and seeds the Admin user):

```bash
export FLASK_APP=app.py
flask init-db
```

Run the Flask API server:

```bash
flask run --port 5000
```

The backend will be available at `http://localhost:5000`.

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

### 3. Background Jobs (Celery & Redis)

Ensure your Redis server is running (default port 6379).

Open a third terminal, activate the backend virtual environment, and start the Celery worker:

```bash
cd backend
source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

## Default Credentials

- **Admin:**
  - Username: `admin`
  - Password: `admin123`

## Features

- **Admin:** Manage doctors, patients, and departments. View hospital analytics.
- **Doctor:** View appointments, complete consultations (diagnosis & prescription), manage availability.
- **Patient:** Search doctors, book appointments, view medical history and prescriptions.
