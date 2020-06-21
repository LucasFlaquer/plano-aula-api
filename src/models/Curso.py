from mongoengine import Document, StringField, ReferenceField

from src.models.User import User


class Curso(Document):
    nome: StringField()
    # diurno vespertino e noturno (D V N)
    turno: StringField(max_length=1)
    coordenador: ReferenceField(User)
