from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.Curso import Curso
from src.models.User import User
from src.services.CursoService import CursoService


@jwt_required
def get_curso_from_user():
    coord: User = User.objects(id=get_jwt_identity()).get()
    curso: Curso = Curso.objects(coordenador=coord).get()

    return jsonify(curso.to_dict_first_grade())


@jwt_required
def get_coordenadores():
    coordenadores: [User] = User.objects(access__coordenador=True)
    user_list = []
    for coord in coordenadores:
        user_list.append(coord.to_dict())
    return jsonify(user_list)


def return_curso_not_found():
    output = {"error": {"msg": "500 error: Curso não encontrado."}}
    resp: object = jsonify({'result': output})
    resp.status_code = 500
    return resp
