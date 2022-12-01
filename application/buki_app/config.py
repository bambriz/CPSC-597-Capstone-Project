import os

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = 'sqlite:///buki_app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
