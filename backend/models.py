from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'doctor', 'patient'
    is_active = db.Column(db.Boolean, default=True)
    
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    patient_profile = db.relationship('Patient', backref='user', uselist=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    doctors = db.relationship('Doctor', backref='department', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    availability = db.Column(db.JSON) # Store availability as JSON, e.g., {"Mon": ["10:00", "12:00"]}
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_of_birth = db.Column(db.Date)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Booked') # Booked, Completed, Cancelled
    
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
