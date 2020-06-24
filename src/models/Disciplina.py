from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField


# class CodTurno(EmbeddedDocument):
#     cod = StringField(required=True)
#     turno = StringField(max_length=1, required=True)


class Disciplina(Document):
    nome = StringField()
    codigo = StringField(required=True)
    turno = StringField(max_length=1)
