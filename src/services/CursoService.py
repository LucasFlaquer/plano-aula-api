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