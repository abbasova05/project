from flask import Flask, request, render_template, redirect, url_for, flash, session
import re
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def is_password_valid(password):
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        sifre = request.form.get('sifre')
        remember = request.form.get('remember')

        users = load_users()
        user = users.get(email)

        if not user or user['sifre'] != sifre:
            flash('Email və ya şifrə səhvdir.', 'error')
            return redirect(url_for('login'))

        session['user'] = email
        if remember:
            session.permanent = True
        else:
            session.permanent = False

        flash(f'Xoş gəlmisiniz, {user["ad"]}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ad = request.form.get('ad').strip()
        soyad = request.form.get('soyad').strip()
        email = request.form.get('email').strip().lower()
        sifre = request.form.get('sifre')
        tekrar_sifre = request.form.get('tekrar_sifre')

        users = load_users()

        if email in users:
            flash('Bu email ilə artıq qeydiyyat var.', 'error')
            return redirect(url_for('register'))

        if sifre != tekrar_sifre:
            flash('Şifrələr üst-üstə düşmür.', 'error')
            return redirect(url_for('register'))

        if not is_password_valid(sifre):
            flash('Şifrə minimum 6 simvol, böyük, kiçik hərf, rəqəm və xüsusi simvol içərməlidir.', 'error')
            return redirect(url_for('register'))

        users[email] = {
            'ad': ad,
            'soyad': soyad,
            'sifre': sifre
        }
        save_users(users)
        flash('Qeydiyyat uğurla tamamlandı! İndi daxil olun.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Zəhmət olmasa daxil olun.', 'error')
        return redirect(url_for('login'))

    users = load_users()
    user = users.get(session['user'])
    return f"<h1>Salam, {user['ad']} {user['soyad']}! Siz daxil olmusunuz.</h1><a href='/logout'>Çıxış</a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Hesabdan çıxış etdiniz.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)
