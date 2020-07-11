from mongoengine import *

from src.models.Bibliografia import Bibliografia


class Ementa(EmbeddedDocument):
    data = DateTimeField()
    descricao = StringField()
    conteudo = ListField(StringField())
    competencias = ListField(StringField())
    objetivos = ListField(StringField())
    bibliografia_basica = ListField(ReferenceField(Bibliografia))
    bibliografia_complementar = ListField(ReferenceField(Bibliografia))

    def to_dict(self):
        basica = []
        complementar = []
        for lib in self.bibliografia_basica:
            basica.append(dict(id=str(lib.pk), nome=lib.nome, conteudo=lib.conteudo))
        for lib in self.bibliografia_complementar:
            complementar.append(dict(id=str(lib.pk), nome=lib.nome, conteudo=lib.conteudo))
        return dict(
            data=self.data.strftime("%m/%d/%Y, %H:%M:%S"),
            descricao=self.descricao,
            conteudo=self.conteudo,
            competencias=self.competencias,
            objetivos=self.objetivos,
            basica=basica,
            complementar=complementar
        )


class Disciplina(Document):
    nome = StringField(required=True)
    carga_pratica = IntField()
    carga_teoria = IntField()
    semestre = IntField()
    ementas = SortedListField(EmbeddedDocumentField(Ementa), default=[], ordering="data")

    # prof_nde = ReferenceField()

    def to_dict(self):
        return dict(
            id=str(self.pk),
            nome=self.nome,
            teoria=self.carga_teoria,
            pratica=self.carga_pratica,
            semestre=self.semestre,
            ementa=self.ementas[0].to_dict()
        )
