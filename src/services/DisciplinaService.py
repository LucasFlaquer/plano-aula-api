from src.models.Disciplina import Disciplina, ValidationError
from src.services.BibliografiaService import BibliografiaService


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

    @staticmethod
    def add_bibliografia_to_ementa(libs):
        libs_list = []
        for lib_id in libs:
            libs_list.append(BibliografiaService.get_by_id(lib_id))

        return libs_list
