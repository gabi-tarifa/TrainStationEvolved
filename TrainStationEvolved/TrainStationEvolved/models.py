from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, ForeignKeyConstraint

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(255), nullable = False)
    level = db.Column(db.Integer, default = 1)
    language = db.Column(db.String(4), nullable = False, default = "ptbr")
    gold = db.Column(db.Integer, nullable=False, default=0)


    def to_dict (self):
        return {
            "id": self.id_usuario,
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "level": self.level,
            "language": self.language,
        }
    
class Material(db.Model):
    __tablename__ = "Material"

    id_material = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.String(255), nullable=False, default="icon/mat.png")
    kind = db.Column(db.String(20), nullable=False)
    unlocking_level = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": kind,
        "polymorphic_identity": "material"
    }


class RawMaterial(Material):
    __tablename__ = "RawMaterial"

    id_material = db.Column(db.Integer, ForeignKey("Material.id_material"), primary_key = True)

    __mapper_args__ = {
        "polymorphic_identity": "raw"
    }

class FactoryMaterial(Material):
    __tablename__ = "FactoryMaterial"

    id_material = db.Column(db.Integer, ForeignKey("Material.id_material"), primary_key = True)

    __mapper_args__ = {
        "polymorphic_identity": "factory"
    }

class TypeLoco(db.Model):
    __tablename__ = "TypeLoco"

    id_type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    profit = db.Column(db.Integer, nullable=False, default=100) #profit will be divided by a 100 during material/gold calculation, but wil be displayed as the full hundred number
    icon = db.Column(db.String(255), nullable=False, default= "icon/typeloco/type.png")

class Locomotive(db.Model):
    __tablename__ = "Locomotive"

    id_loco = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    id_type = db.Column(db.Integer, ForeignKey("TypeLoco.id_type"), nullable=False)
    model = db.Column(db.String(255), nullable=False, default="icon/trainmodels/train.png")

class Destination(db.Model):
    __tablename__ = "Destination"

    id_dest = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, default="Farm")
    timeTravelMinutes = db.Column(db.Integer, nullable=False, default = 5)
    image = db.Column(db.Integer, nullable=False, default = "img/destinations/idleIMG.png")