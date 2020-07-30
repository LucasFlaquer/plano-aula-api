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

class AtvPeso(EmbeddedDocument):
    atividade = StringField()
    peso = IntField()

class Etapa(EmbeddedDocumentField):
    atividades = ListField(AtvPeso)

class PlanoAula(Document):
    professor = ReferenceField(User)
    disciplina = ReferenceField(Disciplina)
    curso = ReferenceField(Curso)
    turma = StringField()
    turno = StringField()
    data = DateTimeField()
    aulas = SortedListField(EmbeddedDocumentField(Aula), ordering="data")
    #etapas = ListField(Etapa)
    ac1 = ListField(AtvPeso, default=[])
    ac2 = ListField(AtvPeso, default=[])
    af = ListField(StringField(), default=[])
    sub = ListField(StringField(), default=[])


    def to_dict(self):
        aulas_array = []
        for aula in self.aulas:
            aulas_array.append(aula)

        return dict(
            id=str(self.pk),
            professor=dict(id=str(self.professor.pk), nome=self.professor.name),
            disciplina=dict(id=str(self.disciplina.pk), nome=self.disciplina.nome),
            curso=dict(id=str(self.curso.pk), nome=self.curso.nome),
            turno=self.turno,
            turma=self.turma,
            aulas=aulas_array
        )