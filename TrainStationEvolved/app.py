import secrets
from flask import Flask
from flask import app, render_template
from flask_login import current_user, login_required, LoginManager
from flask_cors import CORS
from models import db, User


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

@app.route("/")
def mapa():
    return render_template("index.html")

@login_required
@app.route("/game")
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