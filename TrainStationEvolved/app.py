import secrets
from flask import Flask
from flask import app, render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from flask_cors import CORS
from models import db, User, Locomotive, TypeLoco, TrainWagon, Train, Wagon, Material, RawMaterial, FactoryMaterial
from models import Destination, UserLoco, WagonUser, CargoWagon, PassengerWagon, MaterialUser
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from setup.setup_destinations import create_destinations
from setup.setup_typeloco import create_typeloco
from setup.setup_materials import create_materials
from setup.setup_locos import create_locos
from setup.setup_wagons import create_wagons
from xp_visualiser import xp_to_next_level


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:pass123@localhost:3306/TSE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

with app.app_context():
    db.create_all()
    create_destinations()
    create_typeloco()
    create_materials()
    create_locos()
    create_wagons()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
login_manager.login_message_category = "info"

@app.route("/welcome")
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login_page"))  

@app.route("/")
@login_required
def game():
    user_data = User.query.filter_by(id=current_user.id).first()

    xp_needed = xp_to_next_level(current_user.level)

    return render_template("game.html",
                            gold=user_data.gold,
                            diamonds=user_data.diamonds,
                            passengers=user_data.passengers,
                            mail=user_data.mail,
                            level=user_data.level,
                            xp=user_data.xp,
                            xp_needed=xp_needed,
                            xp_remaining=xp_needed-user_data.xp,
                            )

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("cadastro.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    nick = data.get("nickname")
    password = data.get("password")
    email = data.get("email")
    language = data.get("language")

    if not nick and not password and not email and not language:
        return jsonify({"message": "Por favor preencha todos os campos"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email já cadastrado"}), 400
    
    pass_hash = generate_password_hash(password)

    user = User(nickname=nick, password=pass_hash, email=email, language=language)

    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": f"User {email} cadastrado com sucesso!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email and not password:
        return jsonify({"message":"Por favor preencha os dados corretamente!"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        
        return jsonify({"message":"Login efetuado com sucesso!"}), 200
    else:
        return jsonify({"message":"Não foi possível encontrar o usuário"}), 401
    
@app.route("/page/trains")
@login_required
def trainSpace():
    user_data = User.query.filter_by(id=current_user.id).first()

    local_trains = Train.query.filter_by(id_user=current_user.id, location="L").all()
    it_trains = Train.query.filter_by(id_user=current_user.id, location="I").all()
    depot_trains = Train.query.filter_by(id_user=current_user.id, location="D").all()


    return render_template("page/trains.html",
                            user=user_data,
                            local_slots=user_data.local_slots,
                            it_slots=user_data.it_slots,
                            depot_slots=user_data.depot_slots,
                            )

@app.route("/page/trains/buildTrain")
@login_required
def buildTrain():
    user_data = User.query.filter_by(id=current_user.id).first()

    locos = UserLoco.query.filter_by(id_user=current_user.id).all()
    
    wagons = WagonUser.query.filter_by(id_user=current_user.id).all()

    return render_template("page/createTrain.html",
                            user=user_data,
                            locos=locos,
                            wagons=wagons,
                            )

@app.route("/page/shop")
@login_required
def shop():
    locos = Locomotive.query.all()
    cargowagons = CargoWagon.query.all()
    passwagons = PassengerWagon.query.all()


    locos_data = []

    for loco in locos:
        locked = False
        lock_reason = None
        ownedloco = UserLoco.query.filter_by(
            id_user=current_user.id,
            id_loco=loco.id_loco
        ).first()

        if current_user.level < loco.level_unlocking:
            locked = True
            lock_reason = "level"
        elif loco.id_type == 2 and not current_user.diesel_enabled:
            locked = True
            lock_reason = "diesel"
        elif loco.id_type == 3 and not current_user.electric_enabled:
            locked = True
            lock_reason = "electric"
        elif loco.id_type == 4 and not current_user.maglev_enabled:
            locked = True
            lock_reason = "maglev"
        elif loco.id_type == 5 and not current_user.hyperloop_enabled:
            locked = True
            lock_reason = "hyperloop"

        affordable = current_user.gold >= loco.price

        type_data = TypeLoco.query.filter_by(id_type=loco.id_type).first()

        locos_data.append({
            "id": loco.id_loco,
            "name": loco.name,
            "power": loco.power,
            "profit": type_data.profit,
            "price": loco.price,
            "image": loco.model,
            "type": type_data.name,
            "tax_send": loco.tax_send,
            "limit": loco.limit,
            "owned": ownedloco.quantity if ownedloco else 0,
            "xp_buy": loco.xp_buy,
            "level_unlocking": loco.level_unlocking,

            "locked": locked,
            "lock_reason": lock_reason,
            "affordable": affordable
        })

    passwagons_data = []

    for passwagon in passwagons:
        locked = False
        lock_reason = None
        ownedpasswagon = WagonUser.query.filter_by(
            id_user=current_user.id,
            id_wagon=passwagon.id_wagon
        ).first()

        if current_user.level < passwagon.level_unlocking:
            locked = True
            lock_reason = "level"

        affordable = current_user.gold >= passwagon.price

        passwagons_data.append({
            "id": passwagon.id_wagon,
            "name": passwagon.name,
            "profit": passwagon.profit,
            "price": passwagon.price,
            "image": passwagon.model,
            "passengers": passwagon.passengers,
            "mail": passwagon.mail,
            "xp_buy": passwagon.xp_buy,
            "owned": ownedpasswagon.quantity if ownedpasswagon else 0,


            "locked": locked,
            "lock_reason": lock_reason,
            "affordable": affordable
        })

    cargowagons_data = []

    for cargowagon in cargowagons:
        material=Material.query.filter_by(id_material=cargowagon.id_material).first()

        locked = False
        lock_reason = None
        ownedcargowagon = WagonUser.query.filter_by(
            id_user=current_user.id,
            id_wagon=cargowagon.id_wagon
        ).first()

        if current_user.level < cargowagon.level_unlocking:
            locked = True
            lock_reason = "level"

        affordable = current_user.gold >= cargowagon.price

        cargowagons_data.append({
            "id": cargowagon.id_wagon,
            "name": cargowagon.name,
            "profit": cargowagon.profit,
            "price": cargowagon.price,
            "image": cargowagon.model,
            "xp_buy": cargowagon.xp_buy,
            "material": material.name,
            "owned": ownedcargowagon.quantity if ownedcargowagon else 0,

            "locked": locked,
            "lock_reason": lock_reason,
            "affordable": affordable
        })

    return render_template("page/shop.html", loco=locos_data, cargowagon=cargowagons_data, passwagon=passwagons_data)

@app.route("/api/shop/buy", methods=["POST"])
@login_required
def buy_item():
    data = request.get_json()

    item_type = data.get("type")
    item_id = data.get("id")

    user = User.query.get(current_user.id)

    if item_type == "loco":
        item = Locomotive.query.get(item_id)
    elif item_type == "cargo":
        item = CargoWagon.query.get(item_id)
    elif item_type == "passenger":
        item = PassengerWagon.query.get(item_id)
    else:
        return jsonify(success=False, error="invalid_type"), 400

    price = item.price
    
    if user.gold < price:
        return jsonify(success=False, error="not_enough_gold"), 403
    
    user.gold -= price

    if item_type == "loco":
        ul = UserLoco.query.filter_by(id_user=user.id, id_loco=item.id_loco).first()
        if ul:
            ul.quantity += 1
        else:
            db.session.add(UserLoco(id_user=user.id, id_loco=item.id_loco, quantity=1))

    else:
        wu = WagonUser.query.filter_by(id_user=user.id, id_wagon=item.id_wagon).first()
        if wu:
            wu.quantity += 1
        else:
            db.session.add(WagonUser(id_user=user.id, id_wagon=item.id_wagon, quantity=1))

    xp_data = apply_xp(user, item.xp_buy)

    db.session.commit()

    return jsonify(success=True, new_gold=user.gold, price=price, xp_update=item.xp_buy, **xp_data)

def apply_xp(user, gained_xp):
    with app.app_context():
        leveled_up = False
        levels_gained = 0

        user.xp += gained_xp

        while user.xp >= xp_to_next_level(user.level):
            user.xp -= xp_to_next_level(user.level)
            user.level += 1
            leveled_up = True
            levels_gained += 1

        xp_needed = xp_to_next_level(user.level)

    return {
        "level": user.level,
        "xp": user.xp,
        "xp_needed": xp_needed,
        "leveled_up": leveled_up,
        "levels_gained": levels_gained
    }

@app.route("/page/warehouse")
def warehouse():
    locos_data = []
    cargo_data = []
    pass_data = []

    ownedLocos = (db.session.query(Locomotive, UserLoco, TypeLoco)
                  .join(UserLoco, Locomotive.id_loco == UserLoco.id_loco)     # get all the loco
                  .join(TypeLoco, Locomotive.id_type == TypeLoco.id_type)     # that user owns
                  .filter(UserLoco.id_user == current_user.id).all())
    ownedCargo = (db.session.query
                  (CargoWagon, WagonUser, Material)
                  .join(WagonUser, CargoWagon.id_material == WagonUser.id_wagon)
                  .join(Material, CargoWagon.id_material == Material.id_material)                   # get all the cargo wagons
                  .filter(WagonUser.id_user == current_user.id).all())                              # that user owns
    ownedPass = (db.session.query
                  (Wagon, WagonUser).join(WagonUser, Wagon.id_wagon == WagonUser.id_wagon)          # get all the passengers wagons
                  .filter(Wagon.kind == "passenger", WagonUser.id_user == current_user.id).all())   # that user owns
    for loco, ownloco, typeloco in ownedLocos:

        locos_data.append({
            "id": loco.id_loco,
            "name": loco.name,
            "power": loco.power,
            "profit": typeloco.profit,
            "price": loco.price,
            "image": loco.model,
            "type": typeloco.name,
            "tax_send": loco.tax_send,
            "quantity": ownloco.quantity
        })
    for cargowagon, owncargo, material in ownedCargo:
        cargo_data.append({
            "id": cargowagon.id_wagon,
            "name": cargowagon.name,
            "profit": cargowagon.profit,
            "price": cargowagon.price,
            "image": cargowagon.model,
            "material": material.name,
            "quantity": owncargo.quantity

        })
    for passwagon, ownpass in ownedPass:
        pass_data.append({
            "id": passwagon.id_wagon,
            "name": passwagon.name,
            "profit": passwagon.profit,
            "price": passwagon.price,
            "image": passwagon.model,
            "passengers": passwagon.passengers,
            "mail": passwagon.mail,
            "owned": ownpass.quantity
        })


    return render_template("page/warehouse.html", locos=locos_data, cargowagons=cargo_data, passwagons = pass_data)

@app.route("/hud/tool/materials")
def materials():
    raw_materials = RawMaterial.query.all()
    fac_materials = FactoryMaterial.query.all()

    print(raw_materials)
    print(fac_materials)

    raw_mats_data = []
    fac_mats_data = []

    for mat in raw_materials:
        ownmat = MaterialUser.query.filter_by(
            id_user=current_user.id,
            id_material=mat.id_material
        ).first()

        locked = current_user.level < mat.unlocking_level

        raw_mats_data.append({
            "id": mat.id_material,
            "name": mat.name,
            "icon": mat.icon,
            "quantity": ownmat.quantity if ownmat else 0,
            "locked": locked,
            "level_unlocking": mat.unlocking_level,
        })

    for mat in fac_materials:
        ownmat = MaterialUser.query.filter_by(
            id_user=current_user.id,
            id_material=mat.id_material
        ).first()

        locked = current_user.level < mat.unlocking_level

        fac_mats_data.append({
            "id": mat.id_material,
            "name": mat.name,
            "icon": mat.icon,
            "quantity": ownmat.quantity if ownmat else 0,
            "locked": locked,
            "level_unlocking": mat.unlocking_level,
        })

    return render_template("hud/tool/materials.html", raw_materials=raw_mats_data, fac_materials = fac_mats_data)



if __name__ == "__main__":
    app.run(debug=True)