from backend.extensions import celery, db, mail
from backend.models import User, Appointment, Doctor, Patient
from datetime import datetime, timedelta
from flask_mail import Message
from flask import render_template_string

@celery.task
def send_daily_reminders():
    """Send reminders for appointments scheduled tomorrow."""
    tomorrow = datetime.now().date() + timedelta(days=1)
    appointments = Appointment.query.filter_by(date=tomorrow, status='Booked').all()
    
    count = 0
    for appt in appointments:
        patient_email = appt.patient.user.email
        doctor_name = appt.doctor.user.username
        time_str = appt.time.strftime('%H:%M')
        
        msg = Message(
            subject=f"Appointment Reminder: Dr. {doctor_name}",
            recipients=[patient_email],
            body=f"Dear {appt.patient.user.username},\n\nThis is a reminder for your appointment with Dr. {doctor_name} tomorrow at {time_str}.\n\nPlease arrive 10 minutes early.\n\nRegards,\nHospital Management System"
        )
        try:
            mail.send(msg)
            count += 1
        except Exception as e:
            print(f"Failed to send email to {patient_email}: {e}")
            
    return f"Sent reminders for {count} appointments."

@celery.task
def send_monthly_report():
    """Send monthly activity report to doctors."""
    # For simplicity, we'll just send a summary of their total appointments
    doctors = Doctor.query.all()
    count = 0
    
    for doc in doctors:
        appt_count = len(doc.appointments)
        msg = Message(
            subject="Monthly Activity Report",
            recipients=[doc.user.email],
            body=f"Dear Dr. {doc.user.username},\n\nHere is your monthly activity report.\n\nTotal Appointments: {appt_count}\n\nRegards,\nHospital Management System"
        )
        try:
            mail.send(msg)
            count += 1
        except Exception as e:
            print(f"Failed to send report to {doc.user.email}: {e}")
            
    return f"Monthly reports sent to {count} doctors."

@celery.task
def export_patient_history(patient_id):
    """Export patient history to CSV and email it."""
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found"
        
    # Generate CSV content
    csv_content = "Date,Time,Doctor,Diagnosis,Prescription\n"
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    
    for appt in appointments:
        doctor_name = appt.doctor.user.username
        diagnosis = appt.treatment.diagnosis if appt.treatment else "N/A"
        prescription = appt.treatment.prescription if appt.treatment else "N/A"
        csv_content += f"{appt.date},{appt.time},{doctor_name},{diagnosis},{prescription}\n"
        
    msg = Message(
        subject="Your Medical History Export",
        recipients=[patient.user.email],
        body=f"Dear {patient.user.username},\n\nPlease find attached your medical history export.\n\nRegards,\nHospital Management System"
    )
    
    msg.attach("medical_history.csv", "text/csv", csv_content)
    
    try:
        mail.send(msg)
        return f"Export sent to {patient.user.email}"
    except Exception as e:
        return f"Failed to send export: {e}"
