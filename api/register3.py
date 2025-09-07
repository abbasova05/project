#isdemir nese problem var

from flask import Flask, request, render_template, redirect, url_for, flash
import csv
import os
app = Flask(__name__)
app.secret_key = 'supersecretkey123'
CSV_FILE = 'users.csv'
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ad', 'soyad', 'email', 'username', 'password'])

def read_users():
    users = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users
def write_users(users):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['username','password'])
        writer.writeheader()
        writer.writerows(users)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if action == 'login':
            users = read_users()
            for user in users:
                if user['username'] == username and user['password'] == password:
                    flash('Xoş gəlmisiniz!', 'success')
                    return redirect(url_for('success'))
            flash('İstifadəçi adı və ya şifrə səhvdir', 'error')
            return redirect(url_for('index'))
        elif action == 'register':
            return redirect(url_for('register'))
    return render_template('indexx.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ad = request.form.get('ad', '').strip()
        soyad = request.form.get('soyad', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        password_repeat = request.form.get('password_repeat', '').strip()

        print(f"ad={ad}, soyad={soyad}, email={email}, username={username}, password={password}, password_repeat={password_repeat}")

        if not (ad and soyad and email and username and password and password_repeat):
            flash('Bütün sahələri doldurun', 'error')
            return redirect(url_for('register'))

        if password != password_repeat:
            flash('Şifrələr uyğun gəlmir', 'error')
            return redirect(url_for('register'))

        # ... digər yoxlamalar və qeydiyyat


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        new_username = request.form.get('new_username', '').strip()
        new_password = request.form.get('new_password', '').strip()
        if not username:
            flash('Cari istifadəçi adı boş ola bilməz', 'error')
            return redirect(url_for('update'))
        if not new_username and not new_password:
            flash('Yeni istifadəçi adı və ya yeni şifrə daxil edin', 'error')
            return redirect(url_for('update'))
        users = read_users()
        user_found = False
        if new_username and any(user['username'] == new_username for user in users):
            flash('Yeni istifadəçi adı artıq mövcuddur', 'error')
            return redirect(url_for('update'))
        updated_users = []
        for user in users:
            if user['username'] == username:
                user_found = True
                user['username'] = new_username if new_username else user['username']
                user['password'] = new_password if new_password else user['password']
            updated_users.append(user)
        if not user_found:
            flash('İstifadəçi tapılmadı', 'error')
            return redirect(url_for('update'))
        write_users(updated_users)
        flash('Məlumatlar uğurla yeniləndi', 'success')
        return redirect(url_for('success'))
    return render_template('updatee.html')
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = read_users()
        filtered_users = [user for user in users if user['username'] != username]
        if len(filtered_users) == len(users):
            flash('İstifadəçi tapılmadı', 'error')
            return redirect(url_for('delete'))
        write_users(filtered_users)
        flash('İstifadəçi silindi', 'success')
        return redirect(url_for('index'))
    return render_template('delete.html')
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        new_password = request.form.get('new_password', '').strip()
        if not username or not new_password:
            flash('Bütün sahələri doldurun', 'error')
            return redirect(url_for('reset_password'))
        users = read_users()
        found = False
        for user in users:
            if user['username'] == username:
                user['password'] = new_password
                found = True
        if not found:
            flash('İstifadəçi tapılmadı', 'error')
            return redirect(url_for('reset_password'))
        write_users(users)
        flash('Şifrə uğurla yeniləndi', 'success')
        return redirect(url_for('index'))
    return render_template('reset_password.html')
@app.route('/success')
def success():
    return render_template('succes.html')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=1453)