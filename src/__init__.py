from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import (JWTManager)

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'planoaula',
    'host': 'mongodb+srv://admin:admin123@cluster0-yrk3h.mongodb.net/planoaula?retryWrites=true&w=majority',
}

db = MongoEngine(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

from src import routes
