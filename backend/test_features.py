import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db, cache
from backend.models import User, Doctor, Patient, Appointment
from backend.tasks import send_daily_reminders
from werkzeug.security import generate_password_hash

app = create_app()

def setup_test_data():
    print("\n--- Setting up Test Data ---")
    with app.app_context():
        doc_user = User.query.filter_by(email='testdoc@example.com').first()
        if not doc_user:
            doc_user = User(username='testdoc', email='testdoc@example.com', password_hash=generate_password_hash('password'), role='doctor')
            db.session.add(doc_user)
            db.session.commit()
            doctor = Doctor(user_id=doc_user.id, specialization='General')
            db.session.add(doctor)
            db.session.commit()
            print("Created test doctor.")
        else:
            doctor = Doctor.query.filter_by(user_id=doc_user.id).first()
            if not doctor:
                doctor = Doctor(user_id=doc_user.id, specialization='General')
                db.session.add(doctor)
                db.session.commit()
                print("Created missing doctor profile.")

        pat_user = User.query.filter_by(email='testpat@example.com').first()
        if not pat_user:
            pat_user = User(username='testpat', email='testpat@example.com', password_hash=generate_password_hash('password'), role='patient')
            db.session.add(pat_user)
            db.session.commit()
            patient = Patient(user_id=pat_user.id, date_of_birth=datetime(1990, 1, 1))
            db.session.add(patient)
            db.session.commit()
            print("Created test patient.")
        else:
            patient = Patient.query.filter_by(user_id=pat_user.id).first()
            if not patient:
                patient = Patient(user_id=pat_user.id, date_of_birth=datetime(1990, 1, 1))
                db.session.add(patient)
                db.session.commit()
                print("Created missing patient profile.")

        tomorrow = datetime.now().date() + timedelta(days=1)
        appt = Appointment.query.filter_by(doctor_id=doctor.id, patient_id=patient.id, date=tomorrow).first()
        if not appt:
            appt = Appointment(
                doctor_id=doctor.id,
                patient_id=patient.id,
                date=tomorrow,
                time=datetime.strptime('10:00', '%H:%M').time(),
                status='Booked'
            )
            db.session.add(appt)
            db.session.commit()
            print(f"Created appointment for {tomorrow} at 10:00.")
        else:
            print(f"Appointment already exists for {tomorrow}.")

def test_email_trigger():
    print("\n--- Testing Email Trigger (Celery) ---")
    with app.app_context():
        print("Triggering 'send_daily_reminders' task...")
        
        
        task = send_daily_reminders.delay()
        print(f"Task triggered with ID: {task.id}")
        
        try:
            result = task.get(timeout=10)
            print(f"Task Result: {result}")
            
            if "Sent reminders for" in str(result):
                count = int(str(result).split()[3])
                if count > 0:
                    print("✅ Successfully sent reminders!")
                else:
                    print("⚠️ Task ran but sent 0 reminders. Check logs for 'Failed to send email'.")
                    print("This is expected if MAIL credentials are not configured.")
        except Exception as e:
            print(f"❌ Task execution failed or timed out: {e}")

if __name__ == "__main__":
    setup_test_data()
    test_email_trigger()
