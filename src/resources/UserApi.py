from flask import jsonify
from flask_restful import Resource

from src.models.User import User


class UserApi(Resource):
    @staticmethod
    def get():
        output = User.objects()
        return jsonify({'result': output})
