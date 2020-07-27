from mongoengine import EmbeddedDocument, Document, StringField, ListField, SortedListField, DateTimeField, IntField, \
    ReferenceField, EmbeddedDocumentField

from src.models.Curso import Curso
from src.models.Disciplina import Disciplina
from src.models.User import User


class Aula(EmbeddedDocument):
    titulo = StringField()
    data = DateTimeField()
    objetivos = ListField(StringField())
    competencias = ListField(IntField())
    estrategia = StringField()
    avaliacao = StringField()
    recursos = StringField()
    tipo = StringField()
    roteiro = StringField()

    def to_dict(self):
        data = self.data.strftime("%m/%d/%Y, %H:%M:%S")
        self.data = data
        return self


class PlanoAula(Document):
    proferssor = ReferenceField(User)
    disciplina = ReferenceField(Disciplina)
    curso = ReferenceField(Curso)
    cod_turma = StringField()
    turno = StringField()
    aulas = SortedListField(EmbeddedDocumentField(Aula), ordering="data")

    def to_dict(self):
        aulas_array = []
        for aula in self.aulas:
            aulas_array.append(aula)

        return dict(
            id=str(self.pk),
            professor=str(self.proferssor.pk),
            disciplina=self.disciplina.nome,
            curos=self.curso.nome,
            turno=self.turno,
            aulas=aulas_array
        )