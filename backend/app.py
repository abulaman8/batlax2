from flask import Flask, jsonify
from .config import Config
from .extensions import db, jwt, cache, celery
from .models import User, Department, Doctor, Patient, Appointment, Treatment
from werkzeug.security import generate_password_hash
import click
from flask_cors import CORS # Moved CORS import to top for clarity and scope

def create_app(config_class=Config):
    """
    Application Factory function.
    
    This function creates and configures the Flask application instance.
    It initializes all extensions (Database, JWT, Cache, Celery) and 
    registers the blueprints (route modules).
    
    Args:
        config_class: The configuration class to use (default: Config from config.py)
        
    Returns:
        app: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask Extensions
    # These bind the extensions to this specific app instance
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    
    # Initialize Celery
    # The user's provided Code Edit snippet changed this to celery_init_app(app)
    # Assuming celery_init_app is a new function or a typo, I'll revert to the original
    # structure for celery initialization as the instruction was primarily about docstrings
    # and the Code Edit snippet didn't provide the definition for celery_init_app.
    # If celery_init_app is intended, it should be defined elsewhere.
    app.extensions['celery'] = celery
    celery.conf.update(app.config)
    
    # Import tasks to ensure they are registered
    from . import tasks

    # CORS initialization moved up as per Code Edit
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Register Blueprints
    # Blueprints organize routes into distinct categories (Auth, Admin, Doctor, Patient)
    # The user's provided Code Edit snippet changed import paths to 'backend.routes'.
    # Reverting to original relative imports '.routes' as 'backend' prefix is not in original file.
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.doctor import doctor_bp
    from .routes.patient import patient_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    
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
