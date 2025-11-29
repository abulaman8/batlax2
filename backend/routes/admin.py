from flask import Blueprint, request, jsonify
from backend.models import User, Doctor, Patient, Department, Appointment
from backend.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        import json
        current_user = json.loads(get_jwt_identity())
        if current_user['role'] != 'admin':
            return jsonify({"msg": "Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_stats():
    """
    Get system statistics for the Admin Dashboard.
    
    Returns:
        JSON object with counts of doctors, patients, and appointments.
    """
    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    
    return jsonify({
        "doctors": doctor_count,
        "patients": patient_count,
        "appointments": appointment_count
    }), 200

@admin_bp.route('/doctors', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_doctors():
    """
    Manage Doctors (List and Add).
    
    GET: Returns a list of all doctors.
    POST: Creates a new doctor account. Expects JSON: { "username", "email", "password", "specialization" }
    """
    if request.method == 'GET':
        doctors = Doctor.query.all()
        result = []
        for doc in doctors:
            result.append({
                "id": doc.id,
                "username": doc.user.username,
                "email": doc.user.email,
                "specialization": doc.specialization,
                "department": doc.department.name if doc.department else None,
                "is_active": doc.user.is_active
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        specialization = data.get('specialization')
        department_id = data.get('department_id')
        
        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "User already exists"}), 400
            
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            role='doctor'
        )
        db.session.add(new_user)
        db.session.commit()
        
        new_doctor = Doctor(
            user_id=new_user.id,
            specialization=specialization,
            department_id=department_id
        )
        db.session.add(new_doctor)
        db.session.commit()
        
        return jsonify({"msg": "Doctor added successfully"}), 201

@admin_bp.route('/doctors/<int:doctor_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@admin_required
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == 'DELETE':
        doctor.user.is_active = False
        db.session.commit()
        return jsonify({"msg": "Doctor deactivated"}), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        doctor.specialization = data.get('specialization', doctor.specialization)
        doctor.department_id = data.get('department_id', doctor.department_id)
        if 'email' in data:
            doctor.user.email = data['email']
        
        db.session.commit()
        return jsonify({"msg": "Doctor updated"}), 200

@admin_bp.route('/patients', methods=['GET'])
@jwt_required()
@admin_required
def get_patients():
    patients = Patient.query.all()
    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "username": p.user.username,
            "email": p.user.email,
            "contact": p.contact_number,
            "is_active": p.user.is_active
        })
    return jsonify(result), 200

@admin_bp.route('/departments', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_departments():
    if request.method == 'GET':
        depts = Department.query.all()
        return jsonify([{"id": d.id, "name": d.name, "description": d.description} for d in depts]), 200
        
    if request.method == 'POST':
        data = request.get_json()
        dept = Department(name=data['name'], description=data.get('description'))
        db.session.add(dept)
        db.session.commit()
        return jsonify({"msg": "Department added"}), 201
