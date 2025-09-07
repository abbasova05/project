#isdemir

from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
import re
app = Flask(__name__)
app.secret_key = 'register-secret-key'
CSV_FILE = 'users.csv'
# Fayl yoxdursa, başlıqla birlikdə yaradılır
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['firstname', 'lastname', 'email', 'password'])
def read_users():
    users = []
    if not os.path.exists(CSV_FILE):
        return users
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users
def write_user(user):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['firstname', 'lastname', 'email', 'password'])
        writer.writerow(user)
def write_users(users):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['firstname', 'lastname', 'email', 'password'])
        writer.writeheader()
        writer.writerows(users)
# Email doğrulama: gmail.com və mail.com domenləri üçün
def valid_email(email):
    pattern = r'^[\w\.-]+@((gmail\.com)|(mail\.com))$'
    return re.match(pattern, email)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        if not firstname or not lastname or not email or not password or not confirm_password:
            flash("Bütün sahələri doldurun", "error")
            return redirect(url_for('register'))
        if not valid_email(email):
            flash("Email yalnız @gmail.com və ya @mail.com ilə bitməlidir", "error")
            return redirect(url_for('register'))
        if password != confirm_password:
            flash("Şifrələr eyni deyil", "error")
            return redirect(url_for('register'))
        if len(password) < 6:
            flash("Şifrə ən azı 6 simvoldan ibarət olmalıdır", "error")
            return redirect(url_for('register'))
        if not re.search(r'[!@#$%*+=\-_<?/]', password):
            flash("Şifrə ən azı 1 xüsusi simvol (!@#$%*+=-_<?/) daxil etməlidir", "error")
            return redirect(url_for('register'))
        users = read_users()
        if any(user['email'] == email for user in users):
            flash("Bu email artıq qeydiyyatdan keçib", "error")
            return redirect(url_for('register'))
        write_user({
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password
        })
        flash("Qeydiyyat uğurla tamamlandı!", "success")
        return redirect(url_for('success'))
    return render_template('register.html')
@app.route('/success')
def success():
    return "<h2>Qeydiyyat uğurla başa çatdı!</h2>"
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        users = read_users()
        filtered_users = [user for user in users if user['email'] != email]
        if len(filtered_users) == len(users):
            flash('İstifadəçi tapılmadı', 'error')
            return redirect(url_for('delete'))
        write_users(filtered_users)
        flash('Hesab uğurla silindi', 'success')
        return redirect(url_for('register'))
    return render_template('delete.html')
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        if not email or not new_password or not confirm_password:
            flash('Bütün sahələri doldurun', 'error')
            return redirect(url_for('reset_password'))
        if new_password != confirm_password:
            flash('Şifrələr eyni deyil', 'error')
            return redirect(url_for('reset_password'))
        if len(new_password) < 6:
            flash("Şifrə ən azı 6 simvoldan ibarət olmalıdır", "error")
            return redirect(url_for('reset_password'))
        if not re.search(r'[!@#$%*+=\-_<?/]', new_password):
            flash("Şifrə ən azı 1 xüsusi simvol (!@#$%*+=-_<?/) daxil etməlidir", "error")
            return redirect(url_for('reset_password'))
        users = read_users()
        found = False
        for user in users:
            if user['email'] == email:
                user['password'] = new_password
                found = True
                break
        if not found:
            flash('İstifadəçi tapılmadı', 'error')
            return redirect(url_for('reset_password'))
        write_users(users)
        flash('Şifrə uğurla yeniləndi', 'success')
        return redirect(url_for('register'))
    return render_template('reset_password.html')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=1453)
