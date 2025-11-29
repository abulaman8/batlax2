from flask import Blueprint, request, jsonify
from backend.models import User, Doctor, Appointment, Patient, Treatment
from backend.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__, url_prefix='/api/doctor')

def get_current_doctor():
    import json
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'doctor':
        return None
    return Doctor.query.filter_by(user_id=current_user['id']).first()

@doctor_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    """
    Get appointments for the currently logged-in doctor.
    
    Returns:
        List of appointments with patient details and status.
    """
    doctor = get_current_doctor()
    if not doctor:
        return jsonify({"msg": "Doctors only"}), 403
        
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date, Appointment.time).all()
    result = []
    for appt in appointments:
        result.append({
            "id": appt.id,
            "patient_name": appt.patient.user.username,
            "date": appt.date.isoformat(),
            "time": appt.time.isoformat(),
            "status": appt.status
        })
    return jsonify(result), 200

@doctor_bp.route('/appointments/<int:appt_id>/complete', methods=['POST'])
@jwt_required()
def complete_appointment(appt_id):
    """
    Mark an appointment as completed and add treatment details.
    
    Args:
        appt_id: ID of the appointment to complete.
    Expects JSON: { "diagnosis": "...", "prescription": "...", "notes": "..." }
    """
    doctor = get_current_doctor()
    if not doctor:
        return jsonify({"msg": "Doctors only"}), 403
        
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor_id != doctor.id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    data = request.get_json()
    
    appt.status = 'Completed'
    
    treatment = Treatment(
        appointment_id=appt.id,
        diagnosis=data.get('diagnosis'),
        prescription=data.get('prescription'),
        notes=data.get('notes')
    )
    
    db.session.add(treatment)
    db.session.commit()
    
    return jsonify({"msg": "Appointment completed"}), 200

@doctor_bp.route('/availability', methods=['GET', 'POST'])
@jwt_required()
def manage_availability():
    doctor = get_current_doctor()
    if not doctor:
        return jsonify({"msg": "Doctors only"}), 403
        
    if request.method == 'GET':
        return jsonify(doctor.availability or {}), 200
        
    if request.method == 'POST':
        data = request.get_json()
        doctor.availability = data
        db.session.commit()
        return jsonify({"msg": "Availability updated"}), 200

@doctor_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_my_patients():
    doctor = get_current_doctor()
    if not doctor:
        return jsonify({"msg": "Doctors only"}), 403
        
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = set([a.patient_id for a in appointments])
    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()
    
    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "username": p.user.username,
            "email": p.user.email,
            "contact": p.contact_number
        })
    return jsonify(result), 200
