from flask import Flask, jsonify
from .config import Config
from .extensions import db, jwt, cache, celery
from .models import User, Department, Doctor, Patient, Appointment, Treatment
from werkzeug.security import generate_password_hash
import click

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    
    # Initialize Celery
    app.extensions['celery'] = celery
    celery.conf.update(app.config)
    
    # Import tasks to ensure they are registered
    from . import tasks

    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.doctor import doctor_bp
    from .routes.patient import patient_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    
    from flask_cors import CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"INVALID TOKEN ERROR: {error}")
        return jsonify({"msg": "Invalid token", "error": str(error)}), 422
        
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"MISSING TOKEN ERROR: {error}")
        return jsonify({"msg": "Missing token", "error": str(error)}), 401

    @app.cli.command("init-db")
    def init_db():
        """Initialize the database and seed admin user."""
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(role='admin').first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            
        admin = User(
            username='admin',
            email='admin@hospital.com',
            password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Initialized database and created admin user.")

    @app.route('/')
    def index():
        return "Hospital Management System API"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
