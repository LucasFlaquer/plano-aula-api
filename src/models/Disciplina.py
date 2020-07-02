from mongoengine import *

from src.models.Bibliografia import Bibliografia


class Ementa(EmbeddedDocument):
    data = DateTimeField()
    descricao = StringField()
    conteudo = ListField(StringField())
    competencias = ListField(StringField())
    objetivos = ListField(StringField())
    # bibliografia_basica = ListField(ReferenceField(Bibliografia))
    # bibliografia_complementar = ListField(ReferenceField(Bibliografia))


class Disciplina(Document):
    nome = StringField(required=True)
    carga_pratica = IntField()
    carga_teoria = IntField()
    semestre = IntField()
    ementas = SortedListField(EmbeddedDocumentField(Ementa), default=[], ordering="data")

    # prof_nde = ReferenceField()

    def to_dict(self):
        return dict(
            id=self.pk,
            nome=self.nome,
            teoria=self.carga_teoria,
            pratica=self.carga_pratica,
            ementa=self.ementas[0]
        )
