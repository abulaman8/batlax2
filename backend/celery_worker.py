from backend.app import create_app
from backend.extensions import celery

app = create_app()
app.app_context().push()
