import json

from mongoengine import *

from src.models.Disciplina import Disciplina
from src.models.User import User


class Grade(EmbeddedDocument):
    ano = IntField()
    disciplinas = ListField(ReferenceField(Disciplina))

    def to_dict(self):
        disciplinas_dict = []
        disc: Disciplina
        for disc in self.disciplinas:
            disciplinas_dict.append(dict(id=str(disc.id), nome=disc.nome, semestre=disc.semestre))
        print(disciplinas_dict)
        return dict(ano=self.ano, disciplinas=disciplinas_dict)


class Curso(Document):
    nome = StringField(required=True)
    coordenador = ReferenceField(User, default=None)
    publico = BooleanField(default=True)
    grades = SortedListField(EmbeddedDocumentField(Grade), ordering="ano")

    def to_dict(self) -> object:
        grades_dict = []
        grade: Grade
        for grade in self.grades:
            grades_dict.append(grade.to_dict())

        return dict(
            id=str(self.pk),
            nome=self.nome,
            coordenador=dict(id=str(self.coordenador.pk), nome=self.coordenador.name),
            grades=grades_dict

        )

    def to_dict_first_grade(self):
        return dict(
            id=str(self.pk),
            nome=self.nome,
            coordenador=dict(id=str(self.coordenador.pk), nome=self.coordenador.name),
            grades=[self.grades[0].to_dict()]

        )