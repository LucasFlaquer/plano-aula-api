from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import EmbeddedDocument, BooleanField, Document, EmailField, StringField, ListField, ReferenceField

from src.models.Disciplina import Disciplina, EmbeddedDocumentField


class Access(EmbeddedDocument):
    coordenador = BooleanField(default=False)
    nde = BooleanField(default=False)
    qualidade = BooleanField(default=False)
    admin = BooleanField(default=False)


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField()
    password = StringField(required=True, min_length=6, regex=None)
    access = EmbeddedDocumentField(Access, default=Access(coordenador=False, nde=False, qualidade=False, admin=False))
    disciplinas_ministradas = ListField(ReferenceField(Disciplina), default=[])

    def check_pwd(self, pwd):
        if pwd == self.password:
            return True

    def to_dict(self):
        disciplinas_dict = []
        disc: Disciplina
        for disc in self.disciplinas_ministradas:
            disciplinas_dict.append(dict(id=str(disc.id), nome=disc.nome, semestre=disc.semestre))
        return dict(
            id=str(self.pk),
            name=self.name,
            email=self.email,
            password=self.password,
            access=self.access,
            disciplinas_ministradas=disciplinas_dict
        )
