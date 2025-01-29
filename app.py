from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

client = MongoClient(os.getenv("MONGO_URI"))
db = client["PassGuard"]
users_col = db["users"]

class User(UserMixin):
    def __init__(self, user_id):
        self.id = str(user_id)

@login_manager.user_loader
def load_user(user_id):
    user_data = users_col.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_id)
    return None


@app.route('/')
def home():
    return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
        
        if users_col.find_one({"email": email}):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        users_col.insert_one({"username": username, "email": email, "password": password, "stored_passwords": []})
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users_col.find_one({"email": email})
        
        if user and bcrypt.check_password_hash(user["password"], password):
            login_user(User(str(user["_id"])))
            return redirect(url_for("generator"))
        
        flash("Invalid credentials.", "danger")
    
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True) 