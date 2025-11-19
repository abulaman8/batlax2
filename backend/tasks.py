from backend.extensions import celery, db
from backend.models import User, Appointment, Doctor, Patient
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

@celery.task
def send_daily_reminders():
    """Send reminders for appointments scheduled today."""
    today = datetime.now().date()
    appointments = Appointment.query.filter_by(date=today, status='Booked').all()
    
    for appt in appointments:
        patient_email = appt.patient.user.email
        msg = f"Reminder: You have an appointment with Dr. {appt.doctor.user.username} at {appt.time} today."
        # In a real app, send email here
        print(f"Sending email to {patient_email}: {msg}")
    
    return f"Sent reminders for {len(appointments)} appointments."

@celery.task
def send_monthly_report():
    """Send monthly activity report to doctors."""
    # Logic to generate HTML report and send email
    doctors = Doctor.query.all()
    for doc in doctors:
        # Generate report
        print(f"Sending monthly report to Dr. {doc.user.username}")
    return "Monthly reports sent."

@celery.task
def export_patient_history(patient_id):
    """Export patient history to CSV."""
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found"
        
    # Generate CSV logic
    print(f"Exporting history for patient {patient.user.username}")
    # Send alert/email with link
    return "Export complete"
