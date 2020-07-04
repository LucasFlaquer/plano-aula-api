from mongoengine import Document, StringField


class Bibliografia(Document):
    nome = StringField(required=True, unique=True)
    autor = StringField()
    editora = StringField()

    def to_dict(self):
        return dict(
            id=str(self.pk),
            nome=self.nome,
            autor=self.autor,
            editora=self.editora
        )
