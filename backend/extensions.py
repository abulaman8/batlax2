from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery import Celery
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()
migrate = Migrate()

def make_celery(app_name=__name__):
    return Celery(app_name, backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

celery = make_celery()
