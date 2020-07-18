from flask import jsonify
from mongoengine import ValidationError

from src.models.User import User


class UserService:
    @staticmethod
    def get_by_id(id):
        try:
            user = User.objects(id=id).get()
            return user
        except (User.DoesNotExist, ValidationError):
            return None

    @staticmethod
    def getUsers():
        users = User.objects()
        ListUsers=[]
        for user in users:
            ListUsers.append(user.to_dict())
        return ListUsers
