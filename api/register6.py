from flask import Flask, render_template
import csv
import os

app = Flask(__name__)
CSV_FILE = 'register.csv'
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['firstname', 'lastname', 'email', 'password'])

@app.route('/')
def home():

    return render_template('1.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=1453)

