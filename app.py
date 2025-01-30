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

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def rail_fence_cipher(text, num_rails):
    rail = [['\n' for _ in range(len(text))] for _ in range(num_rails)]
    dir_down = None
    row, col = 0, 0

    for i in range(len(text)):
        if row == 0:
            dir_down = True
        if row == num_rails - 1:
            dir_down = False
        rail[row][col] = text[i]
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    result = []
    for r in range(num_rails):
        for c in range(len(text)):
            if rail[r][c] != '\n':
                result.append(rail[r][c])
    return ''.join(result)

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

@app.route('/generator', methods=['GET', 'POST'])
@login_required
def generator():
    encrypted_password = ""
    user = users_col.find_one({"_id": ObjectId(current_user.id)})
    
    if request.method == 'POST':
        username = request.form.get('username', '').lower()
        surname = request.form.get('surname', '').lower()
        dob = request.form.get('dob', '').replace('-', '')
        combined_input = f"{username}{surname}{dob}"
        encryption_option = request.form.get('encryption', '0')

        if encryption_option == '1':  # Caesar Cipher
            shift = int(request.form.get('shift', 0))
            encrypted_password = caesar_cipher(combined_input, shift)
        elif encryption_option == '2':  # Rail Fence Cipher
            num_rails = int(request.form.get('num_rails', 3))
            encrypted_password = rail_fence_cipher(combined_input, num_rails)
        else:
            encrypted_password = combined_input

    return render_template("generator.html", username=user["username"], encrypted_password=encrypted_password)

@app.route('/manager')
@login_required
def manager():
    user = users_col.find_one({"_id": ObjectId(current_user.id)})
    return render_template("manager.html", username=user["username"], passwords=user["stored_passwords"])

@app.route('/add-password', methods=["POST"])
@login_required
def add_password():
    site_name = request.form["site_name"]
    url = request.form["url"]
    username = request.form["username"]
    password = request.form["password"]
    
    new_password_entry = {
        "site_name": site_name,
        "url": url,
        "username": username,
        "password": password
    }
    
    users_col.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$push": {"stored_passwords": new_password_entry}}
    )
    
    flash("Password added successfully.", "success")
    return redirect(url_for("manager"))

@app.route('/edit-password/<password_id>', methods=["GET", "POST"])
@login_required
def edit_password_page(password_id):
    user = users_col.find_one({"_id": ObjectId(current_user.id)})
    passwords = user.get("stored_passwords", [])
    
    password_entry = next((p for p in passwords if p["site_name"] == password_id), None)
    
    if not password_entry:
        flash("Password not found.", "danger")
        return redirect(url_for("manager"))
    
    if request.method == "POST":
        updated_password_entry = {
            "site_name": request.form["site_name"],
            "url": request.form["url"],
            "username": request.form["username"],
            "password": request.form["password"]
        }
        
        users_col.update_one(
            {
                "_id": ObjectId(current_user.id),
                "stored_passwords.site_name": password_id
            },
            {
                "$set": {
                    "stored_passwords.$": updated_password_entry
                }
            }
        )
        
        flash("Password updated successfully.", "success")
        return redirect(url_for("manager"))
    
    return render_template("edit_password.html", password=password_entry)

@app.route('/delete-password/<password_id>', methods=["POST"])
@login_required
def delete_password(password_id):
    result = users_col.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$pull": {"stored_passwords": {"site_name": password_id}}}
    )
    
    if result.modified_count > 0:
        flash("Password deleted successfully.", "success")
    else:
        flash("Password not found.", "danger")
    
    return redirect(url_for("manager")) 

    if __name__ == '__main__':
        app.run(debug=True)
