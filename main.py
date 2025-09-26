from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from user import load_users, save_users
from password import is_strong_password
from dotenv import load_dotenv
import os

# .env faylını yüklə
load_dotenv()

# Flask tətbiqini yarat
app = Flask(__name__)

# Gizli açarı mühit dəyişənindən oxu
app.secret_key = os.getenv("SECRET_KEY")

# Ana səhifə
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/əlaqə")
def əlaqə():
    return render_template("about.html")

# Qeydiyyat
@app.route("/qeydiyyat", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Şifrələr eyni deyil!")
            return redirect(url_for("register"))

        if not is_strong_password(password):
            flash("Şifrə zəifdir! Ən az 8 simvol, böyük/kiçik hərf, rəqəm və xüsusi simvol olmalıdır.")
            return redirect(url_for("register"))

        users = load_users()
        if any(user["email"] == email for user in users):
            flash("Bu email artıq qeydiyyatdan keçib!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        users.append({
            "username": username,
            "surname": surname,
            "email": email,
            "password": hashed_password
        })
        save_users(users)
        session["user"] = email
        flash("Qeydiyyat uğurla tamamlandı!")
        return redirect(url_for("dashboard"))

    return render_template("register.html")

# Giriş
@app.route("/giriş", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users = load_users()
        user = next((u for u in users if u["email"] == email), None)

        if user and check_password_hash(user["password"], password):
            session["user"] = user["email"]
            flash(f"Xoş gəldiniz, {user['username']}!")
            return redirect(url_for("dashboard"))
        else:
            flash("Email və ya şifrə yanlışdır!")
        return redirect(url_for("login"))

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Zəhmət olmasa əvvəlcə daxil olun.")
        return redirect(url_for("login"))

    users = load_users()
    user = next((u for u in users if u["email"] == session["user"]), None)

    if not user:
        flash("İstifadəçi tapılmadı!")
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=user)

# Çıxış
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Siz çıxış etdiniz.")
    return redirect(url_for("login"))

# Əsas giriş nöqtəsi
if __name__ == "__main__":
    app.run(debug=True)
