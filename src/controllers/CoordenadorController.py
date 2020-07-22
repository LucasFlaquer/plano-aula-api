from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.Curso import Curso
from src.models.User import User
from src.services.CursoService import CursoService


@jwt_required
def get_curso_from_user():
    coord: User = User.objects(id=get_jwt_identity()).get()

    # curso = CursoService.
    if coord.access.coordenador:
        curso = Curso.objects(coordenador=coord).get()
    else:
        curso = None
    return jsonify(curso)
