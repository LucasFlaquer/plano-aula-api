from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import Document, StringField, EmailField

class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField()
    password = StringField(required=True, min_length=6, regex=None)

    def check_pwd(self, pwd):
        if pwd == self.password:
            return True
    # def generate_pw_hash(self):
    #     self.password = generate_password_hash(password=self.password).decode('utf-8')
    #
    # generate_pw_hash.__doc__ = generate_password_hash.__doc__
    #
    # def check_pw_hash(self, password: str) -> bool:
    #     print("==============bug")
    #     return check_password_hash(pw_hash=self.password, password=password)
    #
    # # Use documentation from BCrypt for password hashing
    # check_pw_hash.__doc__ = check_password_hash.__doc__