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
    def get_all_as_dict():
        users = User.objects()
        list_users = []
        for user in users:
            list_users.append(user.to_dict())
        return list_users

    @staticmethod
    def getUsers():
        users = User.objects()
        ListUsers = []
        for user in users:
            ListUsers.append(user.to_dict())
        return ListUsers
