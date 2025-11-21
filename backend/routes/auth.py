from flask import Blueprint, request, jsonify
from backend.models import User, Patient, Doctor
from backend.extensions import db, jwt
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        import json
        identity = json.dumps({'id': user.id, 'role': user.role, 'username': user.username})
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token, role=user.role, username=user.username), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expects JSON data: { "username": "...", "email": "...", "password": "...", "role": "patient" }
    Only allows registration for 'patient' role.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'patient') # Default to patient
    
    if role == 'admin':
        return jsonify({"msg": "Admin registration is not allowed"}), 403
        
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400
        
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
        role=role
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    if role == 'patient':
        # Create empty patient profile
        patient = Patient(user_id=new_user.id)
        db.session.add(patient)
        db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    import json
    current_user = json.loads(get_jwt_identity())
    return jsonify(current_user), 200
