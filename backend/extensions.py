from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery import Celery
from flask_mail import Mail

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()

def make_celery(app_name=__name__):
    return Celery(app_name, backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

celery = make_celery()
