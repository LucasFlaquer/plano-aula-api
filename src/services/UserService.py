from flask import jsonify
from mongoengine import ValidationError

from src.models.User import User


class UserService():
    @staticmethod
    def getUserById(id):
        try:
            user = User.objects(id=id).get()
            return user
        except (User.DoesNotExist, ValidationError):
            return None