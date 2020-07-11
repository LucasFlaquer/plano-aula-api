from src.models.Disciplina import Disciplina, ValidationError


class DisciplinaService:

    @staticmethod
    def get_all():
        return Disciplina.objects()

    @staticmethod
    def get_all_as_dict():
        list_disc: [Disciplina] = Disciplina.objects()

        disciplinas = []

        for disc in list_disc:
            disciplinas.append(disc.to_dict())

        return disciplinas

    @staticmethod
    def get_by_id(id):
        try:
            return Disciplina.objects(id=id).get()
        except (Disciplina.DoesNotExists, ValidationError):
            return None
