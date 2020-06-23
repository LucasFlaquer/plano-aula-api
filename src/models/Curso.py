from mongoengine import Document, StringField, ReferenceField

from src.models.User import User


class Curso(Document):
    nome = StringField(required=True)
    # diurno vespertino e noturno (D V N)
    turno = StringField(max_length=1, required=True)
    coordenador = ReferenceField(User)
