from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import os
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'knbs_stanley_2026'
DATABASE = 'census_system.db'

# Full list of 47 Kenyan Counties for the Regions view
COUNTIES = [
    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta", "Garissa", "Wajir", "Mandera", "Marsabit",
    "Isiolo", "Meru", "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga",
    "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", "Elgeyo-Marakwet", "Nandi",
    "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia",
    "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"
]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user' in session: return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.form.get('user')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    db = get_db()
    records = db.execute('SELECT * FROM census_records ORDER BY id DESC').fetchall()
    return render_template('index.html', records=records, counties=COUNTIES, user=session['user'])

@app.route('/export_excel')
def export_excel():
    db = get_db()
    df = pd.read_sql_query("SELECT * FROM census_records", db)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='CensusData')
    output.seek(0)
    return send_file(output, download_name="KNBS_Census_Report.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)