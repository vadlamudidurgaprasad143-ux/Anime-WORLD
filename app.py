from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import random

from models import db, User

app = Flask(__name__)

# ==========================
# FLASK CONFIGURATION
# ==========================
app.config["SECRET_KEY"] = "anime-world-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ==========================
# DATABASE
# ==========================
db.init_app(app)

# ==========================
# LOGIN MANAGER
# ==========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ==========================
# CREATE DATABASE
# ==========================
with app.app_context():
    db.create_all()

# ==========================
# HOME & AUTHENTICATED ROUTES
# ==========================
@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("home.html", username=current_user.username)
    return redirect(url_for("login"))

# ==========================
# ANIME & CARTOON SHOW PAGES
# ==========================
@app.route("/naruto")
@login_required
def naruto():
    return render_template("naruto.html")

@app.route("/pokemon")
@login_required
def pokemon():
    return render_template("pokemon.html")

@app.route("/sololeveling")
@login_required
def solo_leveling():
    return render_template("sololeveling.html")

@app.route("/demonslayer")
@login_required
def demon_slayer():
    return render_template("demon_slayer.html")

@app.route("/jujutsukaisen")
@login_required
def jujutsu_kaisen():
    return render_template("jujutsukaisen.html")

@app.route("/doraemon")
@login_required
def doraemon():
    return render_template("doraemon.html")

@app.route("/shinchan")
@login_required
def shinchan():
    return render_template("shinchan.html")

# ==========================
# LOGIN
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.session.scalar(db.select(User).where(User.username == username))

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid username or password!"
        )

    return render_template("login.html")

# ==========================
# SIGNUP & REGISTER
# ==========================
@app.route("/signup", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # 1. Check if passwords match
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match!")

        # 2. Check if username already exists
        existing_user = db.session.scalar(db.select(User).where(User.username == username))
        if existing_user:
            return render_template("signup.html", error="Username already exists!")

        # 3. Hash password and save new user
        hashed_password = generate_password_hash(password)
        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("home"))

    return render_template("signup.html")

# ==========================
# REAL USER GOOGLE CONNECTION SIMULATION
# ==========================
@app.route("/google-login")
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    # Connect/simulate an authenticated Google profile session dynamically
    # (Generates a unique profile name every time, or map to a persistent session email)
    google_user_email = f"google_user_{random.randint(1000, 9999)}@gmail.com"
    
    # Check if this user exists, if not create them seamlessly
    user = db.session.scalar(db.select(User).where(User.username == google_user_email))
    
    if not user:
        hashed_password = generate_password_hash("google_oauth_secure_pass")
        user = User(
            username=google_user_email,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
    
    # Automatically log them into the system
    login_user(user)
    return redirect(url_for("home"))

# ==========================
# LOGOUT
# ==========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
