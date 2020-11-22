from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import (JWTManager)
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'planoaula',
    'host': 'mongodb+srv://admin:fgeDIMyFcL24etT6@cluster0-yrk3h.mongodb.net/planoaula?retryWrites=true&w=majority',
}

db = MongoEngine(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from src import routes
