from mongoengine import ValidationError

from src.models.Curso import Curso


class CursoService:
    @staticmethod
    def getCursoById(id):
        try:
            curso = Curso.objects(id=id).get()
            return curso
        except (Curso.DoesNotExists, ValidationError):
            return None

    @staticmethod
    def getAll():
        return Curso.objects()