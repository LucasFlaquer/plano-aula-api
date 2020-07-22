from mongoengine import ValidationError

from src.models.Curso import Curso


class CursoService:
    @staticmethod
    def get_curso_by_id(id):
        try:
            curso = Curso.objects(id=id).get()
            return curso
        except (Curso.DoesNotExists, ValidationError):
            return None

    @staticmethod
    def get_all():
        return Curso.objects()


    # @staticmethod
    # def get_by_coord(id_coord):
    #     #sss
    #     #



    # @staticmethod
    # def add_disciplinas_to_grade(list_disciplinas):
    #     disciplinas = [],
