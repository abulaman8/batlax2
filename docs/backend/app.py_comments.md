# Comments extracted from app.py

- Line 7: # Moved CORS import to top for clarity and scope
- Line 26: # Initialize Flask Extensions
- Line 27: # These bind the extensions to this specific app instance
- Line 33: # Initialize Celery
- Line 34: # The user's provided Code Edit snippet changed this to celery_init_app(app)
- Line 35: # Assuming celery_init_app is a new function or a typo, I'll revert to the original
- Line 36: # structure for celery initialization as the instruction was primarily about docstrings
- Line 37: # and the Code Edit snippet didn't provide the definition for celery_init_app.
- Line 38: # If celery_init_app is intended, it should be defined elsewhere.
- Line 42: # Import tasks to ensure they are registered
- Line 45: # CORS initialization moved up as per Code Edit
- Line 48: # Register Blueprints
- Line 49: # Blueprints organize routes into distinct categories (Auth, Admin, Doctor, Patient)
- Line 50: # The user's provided Code Edit snippet changed import paths to 'backend.routes'.
- Line 51: # Reverting to original relative imports '.routes' as 'backend' prefix is not in original file.
- Line 79: # Check if admin exists
