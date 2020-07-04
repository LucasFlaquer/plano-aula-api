from mongoengine import ValidationError

from src.models.Bibliografia import Bibliografia


class BibliografiaService:
    @staticmethod
    def get_all_as_dict():
        bibliografias: Bibliografia = Bibliografia.objects()
        list_bibliografia = []
        for bibliografia in bibliografias:
            list_bibliografia.append(bibliografia.to_dict())
        return list_bibliografia

    @staticmethod
    def get_by_id(id):
        try:
            return Bibliografia.objects(id=id).get()
        except (Bibliografia.DoesNotExists, ValidationError):
            return None