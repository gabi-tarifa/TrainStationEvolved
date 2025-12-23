import secrets
from flask import Flask
from flask import app, render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from flask_cors import CORS
from models import db, User
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from setup.setup_destinations import create_destinations
from setup.setup_typeloco import create_typeloco
from setup.setup_materials import create_materials


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
def mapa():
    return render_template("game.html")

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

if __name__ == "__main__":
    app.run(debug=True)