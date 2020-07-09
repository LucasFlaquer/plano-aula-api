from mongoengine import Document, StringField


class Bibliografia(Document):
    nome = StringField(required=True, unique=True)
    conteudo = StringField

    def to_dict(self):
        return dict(
            id=str(self.pk),
            nome=self.nome,
            conteudo=self.conteudo
        )
