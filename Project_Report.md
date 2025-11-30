# **App Dev Project Report**

## **1. Student Details**

**Name:** [Your Name]
**Roll Number:** [Your Roll Number]
**Email:** [Your Email]
**About Me:** [Brief description about yourself]

---

## **2. Project Details**

### **Project Title: Hospital Management System (HMS)**

### **Problem Statement:**

To design and build a web-based application that streamlines hospital operations by managing doctors, patients, appointments, and medical records. The system aims to facilitate efficient healthcare delivery, reduce administrative overhead, and improve the overall patient experience through digital appointment booking and record keeping.

### **Approach:**

The app was built using **Flask** as the backend framework with a modular structure using Blueprints. The frontend is developed with **Vue.js 3** and **Vite** for a modern, responsive user interface. The system implements **Role-Based Access Control (RBAC)** to distinguish between Admins, Doctors, and Patients. Background tasks are handled using **Celery** and **Redis** for performance optimization.

---

## **3. AI/LLM Declaration**

I used **AI tools** to assist in generating boilerplate code, debugging complex errors, and formatting documentation.
The extent of AI/LLM usage is around **10–15%**, limited to **code suggestions and documentation formatting**.
All final implementation logic, debugging, and integration were done manually.

OR

No use of AI/LLM.

---

## **4. Technologies and Frameworks Used**

| Technology / Library | Purpose |
| :---- | :---- |
| **Flask** | Core backend web framework |
| **SQLAlchemy** | Object Relational Mapper for SQLite database |
| **Flask-JWT-Extended** | User authentication and secure session management (JWT) |
| **Celery & Redis** | Asynchronous background job processing |
| **Vue.js 3** | Frontend JavaScript framework for building the UI |
| **Vite** | Frontend build tool and development server |
| **Bootstrap 5** | Frontend styling and responsive design |
| **SQLite** | Lightweight local database for storing application data |

---

## **5. Database Schema / ER Diagram**

**Tables:**

1.  **User** — stores user authentication details (id, username, email, password_hash, role, is_active)
2.  **Department** — stores hospital departments (id, name, description)
3.  **Doctor** — stores doctor profiles linked to users (id, user_id, department_id, experience_years, availability)
4.  **Patient** — stores patient profiles linked to users (id, user_id, date_of_birth, contact_number, address)
5.  **Appointment** — logs appointments between doctors and patients (id, doctor_id, patient_id, date, time, status)
6.  **Treatment** — stores medical records for appointments (id, appointment_id, diagnosis, prescription, notes, date_created)

**Relationships:**

*   One-to-One → `User → Doctor`
*   One-to-One → `User → Patient`
*   One-to-Many → `Department → Doctor`
*   One-to-Many → `Doctor → Appointment`
*   One-to-Many → `Patient → Appointment`
*   One-to-One → `Appointment → Treatment`

*(Insert ER diagram image here – can be created using [dbdiagram.io](http://dbdiagram.io) or [draw.io](http://draw.io) or any other website)*

---

## **6. API Resource Endpoints**

| Endpoint | Method | Description |
| :---- | :---- | :---- |
| `/login` | POST | Authenticate user and return JWT access token |
| `/register` | POST | Register a new user (Patient role by default) |
| `/api/patient/doctors` | GET | Search for doctors by department |
| `/api/patient/appointments` | GET | Fetch all past and upcoming appointments for the logged-in patient |
| `/api/patient/appointments` | POST | Book a new appointment with a doctor |
| `/api/patient/profile` | GET/PUT | Retrieve or update patient profile details |
| `/api/admin/departments` | GET/POST | Manage hospital departments |

**YAML API Definition File:**
Included separately in the submission ZIP as `api.yaml`.

---

## **7. Architecture and Features**

### **Architecture Overview:**

*   **backend/app.py** – Main Flask application entry point and configuration.
*   **backend/models.py** – Database models defined using SQLAlchemy.
*   **backend/routes/** – Flask Blueprints separating logic for Auth, Patient, Doctor, and Admin.
*   **frontend/src/** – Vue.js source code including Components, Views, and Router.
*   **celery_worker.py** – Entry point for Celery background workers.

### **Implemented Features:**

*   **User Authentication:** Secure login and registration with password hashing and JWT.
*   **Role-Based Access:** Distinct portals for Admins, Doctors, and Patients.
*   **Appointment Booking:** Patients can search for doctors and book appointments.
*   **Medical Records:** Doctors can add diagnoses and prescriptions to appointments.
*   **Profile Management:** Users can update their personal and contact information.
*   **Responsive UI:** A clean and mobile-friendly interface built with Bootstrap 5.

### **Additional Features:**

*   **Background Jobs:** Asynchronous tasks handled by Celery (e.g., email notifications, reminders).
*   **Doctor Availability:** Doctors can manage their available slots.

---

## **8. Video Presentation**

**Drive Link:**
[Insert your Google Drive Video Link Here]
*(Accessible to all with “View” permission.)*
