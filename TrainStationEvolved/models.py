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
    language = db.Column(db.String(4), nullable = False, default = "eng")
    gold = db.Column(db.Integer, nullable=False, default=0)
    mail = db.Column(db.Integer, nullable=False, default=1000)
    xp = db.Column(db.Integer, nullable=False, default=0)
    local_slots = db.Column(db.Integer, nullable=False, default=3) #local trains collect materials and from any destination and send to your station
    it_slots = db.Column(db.Integer, nullable=False, default=0) #IT (International Trains) are locked by default and in level 6
    depot_slots = db.Column(db.Integer, nullable=False, default=6) #depot trains don't do a shit, aside not using warehouse space 
    passengers = db.Column(db.Integer, nullable=False, default=0)

    def to_dict (self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "level": self.level,
            "language": self.language,
        }
    
class Material(db.Model):
    __tablename__ = "Material"

    id_material = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(255), nullable=False, default="icon/material/mat.png")
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
    model = db.Column(db.String(255), nullable=False, default="models/loco/train.png")
    xp_buy = db.Column(db.Integer, nullable=False, default=0)
    xp_send = db.Column(db.Integer, nullable=False, default=0)

class Destination(db.Model):
    __tablename__ = "Destination"

    id_dest = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, default="Farm")
    timeTravelMinutes = db.Column(db.Integer, nullable=False, default = 5)
    image = db.Column(db.String(50), nullable=False, default = "img/destinations/idleIMG.png")

class UserLoco(db.Model):
    __tablename__ = "UserLoco"

    id_user_loco = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    id_loco = db.Column(db.Integer, ForeignKey("Locomotive.id_loco"), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)

class Wagon(db.Model):
    __tablename__ = "Wagon"

    id_wagon = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, default="Wagon")
    model = db.Column(db.String(55), nullable=False, default="models/wagon/wagon.png")
    profit = db.Column(db.Integer, nullable=False, default=100) #profit will be divided by 100 during total calculation
    kind = db.Column(db.String(30), nullable=False)
    xp_buy = db.Column(db.Integer, nullable=False, default=0)

    __mapper_args__ = {
        "polymorphic_on": kind,
        "polymorphic_identity": "material"
    }

class PassengerWagon(Wagon):
    __tablename__ = "PassengerWagon"

    id_wagon = db.Column(db.Integer, ForeignKey("Wagon.id_wagon"), primary_key=True)
    passengers = db.Column(db.Integer)
    mail = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "passenger"
    }

class CargoWagon(Wagon):
    __tablename__ = "CargoWagon"

    id_wagon = db.Column(db.Integer, ForeignKey("Wagon.id_wagon"), primary_key=True)
    id_material = db.Column(db.Integer, ForeignKey("Material.id_material"), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "cargo"
    }

class MaterialUser(db.Model):
    __tablename__ = "MaterialUser"

    id_material_user = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    id_material = db.Column(db.Integer, ForeignKey("Material.id_material"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

class Train(db.Model):
    __tablename__ = "Train"

    id_train = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    id_loco = db.Column(db.Integer, ForeignKey("Locomotive.id_loco"), nullable=False)

class TrainWagon(db.Model):
    __tablename__ = "TrainWagon"

    id_train_wagon = db.Column(db.Integer, primary_key=True)
    id_train = db.Column(db.Integer, ForeignKey("Train.id_train"), nullable=False)
    id_wagon = db.Column(db.Integer, ForeignKey("Wagon.id_wagon"), nullable=False)
    position = db.Column(db.Integer, nullable=False)
