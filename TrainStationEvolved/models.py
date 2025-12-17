from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"

    id_usuario = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(24), nullable = False)
    level = db.Column(db.Integer, default = 1)
    language = db.Column(db.String(4), nullable = False, default = "pt")

    def to_dict (self):
        return {
            "id": self.id_usuario,
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "level": self.level,
            "language": self.language,
        }
                