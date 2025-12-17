import secrets
from flask import Flask
from flask import app, render_template, redirect, url_for, flash
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from flask_cors import CORS
from models import db, User
import pymysql


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:pass123@localhost:3306/TSE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

@app.route("/")
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

@app.route("/game")
@login_required
def mapa():
    return "Mapa do jogo aqui!!"

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run(debug=True)