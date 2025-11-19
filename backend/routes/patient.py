from flask import Blueprint, request, jsonify
from backend.models import User, Patient, Doctor, Appointment, Department, Treatment
from backend.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

patient_bp = Blueprint('patient', __name__, url_prefix='/api/patient')

def get_current_patient():
    import json
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'patient':
        return None
    return Patient.query.filter_by(user_id=current_user['id']).first()

@patient_bp.route('/doctors', methods=['GET'])
@jwt_required()
def search_doctors():
    specialization = request.args.get('specialization')
    query = Doctor.query
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
        
    doctors = query.all()
    result = []
    for doc in doctors:
        result.append({
            "id": doc.id,
            "name": doc.user.username,
            "specialization": doc.specialization,
            "department": doc.department.name if doc.department else None,
            "availability": doc.availability
        })
    return jsonify(result), 200

@patient_bp.route('/appointments', methods=['GET', 'POST'])
@jwt_required()
def manage_appointments():
    patient = get_current_patient()
    if not patient:
        return jsonify({"msg": "Patients only"}), 403
        
    if request.method == 'GET':
        appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        result = []
        for appt in appointments:
            result.append({
                "id": appt.id,
                "doctor_name": appt.doctor.user.username,
                "date": appt.date.isoformat(),
                "time": appt.time.isoformat(),
                "status": appt.status,
                "diagnosis": appt.treatment.diagnosis if appt.treatment else None,
                "treatment": {
                    "prescription": appt.treatment.prescription,
                    "notes": appt.treatment.notes
                } if appt.treatment else None
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        
        try:
            appt_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            appt_time = datetime.strptime(data['time'], '%H:%M').time()
            
            # Check for overlapping appointments (30 min buffer)
            existing_appointments = Appointment.query.filter_by(doctor_id=doctor_id, date=appt_date).all()
            
            req_start = datetime.combine(appt_date, appt_time)
            req_end = req_start + timedelta(minutes=30)
            
            if req_start < datetime.now():
                return jsonify({"msg": "Cannot book appointments in the past"}), 400
            
            for appt in existing_appointments:
                exist_start = datetime.combine(appt.date, appt.time)
                exist_end = exist_start + timedelta(minutes=30)
                
                # Check overlap: (StartA < EndB) and (EndA > StartB)
                if req_start < exist_end and req_end > exist_start:
                     return jsonify({"msg": "Doctor is not available at this time. Please choose a slot at least 30 minutes apart from existing bookings."}), 400

            new_appt = Appointment(
                patient_id=patient.id,
                doctor_id=doctor_id,
                date=appt_date,
                time=appt_time,
                status='Booked'
            )
            db.session.add(new_appt)
            db.session.commit()
            
            return jsonify({"msg": "Appointment booked successfully"}), 201
        except ValueError:
            return jsonify({"msg": "Invalid date or time format"}), 400

@patient_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    patient = get_current_patient()
    if not patient:
        return jsonify({"msg": "Patients only"}), 403
        
    if request.method == 'GET':
        return jsonify({
            "username": patient.user.username,
            "email": patient.user.email,
            "contact": patient.contact_number,
            "address": patient.address,
            "dob": patient.date_of_birth.isoformat() if patient.date_of_birth else None
        }), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        patient.contact_number = data.get('contact', patient.contact_number)
        patient.address = data.get('address', patient.address)
        if 'dob' in data:
            patient.date_of_birth = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            
        db.session.commit()
        return jsonify({"msg": "Profile updated"}), 200
