from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.PlanoAula import PlanoAula, Aula
from src.models.User import User
from src.services.CursoService import CursoService
from src.services.DisciplinaService import DisciplinaService
from src.services.UserService import UserService

@jwt_required
def index_plano_aula():
    #retorna todos os planos de aula do usuario logado no sistema
    data = request.get_json()
    user: User = UserService.get_by_id(get_jwt_identity())
    planos = PlanoAula.objects(professor=user)
    planos_list = []
    plano: PlanoAula
    for plano in planos:
        planos_list.append(plano.to_dict())

    return jsonify(planos_list)



@jwt_required
def store_plano_aula():
    data = request.get_json()
    #colocar o validator aqui
    user = UserService.get_by_id(get_jwt_identity())
    curso = CursoService.get_curso_by_id(data.get('curso_id'))
    disciplina = DisciplinaService.get_by_id(data.get('disc_id'))
    print(data.get('aulas')[0]['titulo'])
    plano_aula = PlanoAula()
    plano_aula.proferssor = user
    plano_aula.curso = curso
    plano_aula.disciplina = disciplina
    plano_aula.turno = data['turno']
    plano_aula.data = datetime.utcnow()
    plano_aula.turma = data.get('codigo')
    for aula_data in data.get('aulas'):
        aula = Aula()
        aula.titulo = aula_data['titulo']
        aula.data = aula_data['data']
        aula.objetivos = aula_data['objetivos']
        aula.competencias = aula_data['competencias']
        aula.estrategia = aula_data['estrategia']
        aula.avaliacao = aula_data['avaliacao']
        aula.recursos = aula_data['recursos']
        aula.tipo = aula_data['tipo']
        aula.roteiro = aula_data['roteiro']
        plano_aula.aulas.append(aula)

    plano_aula.save()
    return jsonify(plano_aula)
