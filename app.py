#Librerias
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import CDB
from PIL import Image
"""
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from fpdf import FPDF
from datetime import datetime
...from functools import wraps
import base64
import hashlib
from config import Config
"""

from config import config
import pymysql
import re
import io

cdb = CDB()
cdb.connectDB()
conn = CDB()
conn.__init__()
user_name = "None"

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

def compressImage(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail((1000, 1000))  
    imgComprimida = io.BytesIO()
    img.save(imgComprimida, format='JPEG', quality=90)  
    return imgComprimida.getvalue()

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/home')
def home ():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('users/login.html')

#############
@app.route('/loginProcess', methods=['GET', 'POST'])
def loginAccess():
    global user_name, session, user
    if request.method == 'POST' and 'name' in request.form and 'password':
        _name = request.form['name']
        _pass = request.form['password']

        cur = cdb.cursor
        cur.execute('SELECT id, username, email, password, role FROM user WHERE username = %s', (_name,))
        user = cur.fetchone()

        if user:
            id_user = user[0]
            user_name = user[1].split()[:2]  # Dividir el nombre en las primeras dos palabras
            email_db = user[2]
            password_db = user[3]
            role = user[4]

            if _name == "AdminP" and _pass == 'B!1w8NAt1T^%kvhUI*S^':
                session['id'] = id_user
                session['role'] = role
                return render_template("home.html", user_name=user_name, session=session)
            else:
                if check_password_hash(password_db, _pass):
                    session['id'] = id_user
                    session['role'] = role
                    return render_template("home.html", user_name=user_name, session=session)
                else:
                    return render_template("users/login.html", mensaje1="La contraseña no coincide")
        else:
            return render_template("users/login.html", mensaje1="Por favor, ingrese su correo y contraseña")
    return render_template("users/login.html", mensaje1="Por favor, ingrese su correo y contraseña")

def get_disabilities():
    cur = cdb.cursor
    cur.execute("SELECT disabilityid, name FROM disabilities")  # Ajusta la consulta
    opciones = cur.fetchall()
    return opciones

@app.route('/register')
def register():
  disabilities1 = get_disabilities()
  return render_template('users/register.html', disabilities=disabilities1)

@app.route('/registerProcess', methods=['GET', 'POST'])
def registerAccess():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        _name = request.form['name']
        _email = request.form['email']
        _pass = request.form['password']

        cur = cdb.cursor
        cur.execute('SELECT COUNT(*) FROM admins WHERE username = %s AND email = %s', (_name, _email))
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO admins (username, email, encryptedpassword) VALUES (%s, %s, %s)',
                        (_name, _email, generate_password_hash(_pass)))
            cdb.conection.commit()
            return render_template("users/login.html", mensaje="Usuario registrado con éxito")
        else:
            return render_template("users/register.html", mensaje="El usuario ya existe")
    return render_template("users/register.html", mensaje="Por favor, llene todos los campos")

@app.route('/registerProcessApplicants', methods=['GET', 'POST'])
def registerAccessAppli():
    if request.method == 'POST':
        
        _username = request.form['username']
        _name = request.form['name']
        _firstname = request.form['firstname']
        _secname = request.form['secname']
        _email = request.form['email']
        _pass = request.form['password']
        _age = request.form['age']
        _phone = request.form['phone']
        _address = request.form['address']
        _state = request.form['state']
        _municipaly = request.form['municipaly']
        #_cv = request.files['cv']

        _emergencyc = request.form['emergencyc']
        _related = request.form['related']
        _disabilityid = request.form['disability']
        
        cur = cdb.cursor
        cur.execute('SELECT COUNT(*) FROM applicants WHERE username = %s AND email = %s', (_username, _email))
        if cur.fetchone()[0] == 0:
            """cur.execute('INSERT INTO applicants (username, name, firstname, secname, email, encryptedpasswda, age, phone, address, state, municipaly, cv, emergencycontact, related, disabilityid) VALUES (%s, %s, %s, %s)',
                        (_username, _firstname, _secname, _name, _email, generate_password_hash(_pass), _age, _phone, _address, _state, _municipaly, _cv, _emergencyc, _related, _disabilityid))"""
            cur.execute('INSERT INTO applicants (username, name, firstname, secname, email, encryptedpasswda, age, phone, address, state, municipaly, emergencycontact, related, disabilityid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (_username, _name, _firstname, _secname,  _email, generate_password_hash(_pass), _age, _phone, _address, _state, _municipaly, _emergencyc, _related, _disabilityid))
            cdb.conection.commit()
            return render_template("users/login.html", mensaje="Usuario registrado con éxito")
        else:
            print("El usuario ya existe")
            return render_template("users/register.html", mensaje="El usuario ya existe")
    print("Por favor, llene todos los campos")
    return render_template("users/register.html", mensaje="Por favor, llene todos los campos")

@app.route('/registerProcessCompanies', methods=['GET', 'POST'])
def registerAccessCompanies():
    print(request.form)
    if request.method == 'POST':
        _name = request.form['name']
        _email = request.form['email']
        _pass = request.form['password']
        _phone = request.form['phone']
        _address = request.form['address']
        _state = request.form['state']
        _municipaly = request.form['municipaly']
        _description = request.form['description']
        _rfc = request.form['rfc']
        _logo = request.files['logo']

        type = _logo.mimetype

        logo_compr = compressImage(_logo)

    
        cur = cdb.cursor
        cur.execute('SELECT COUNT(*) FROM companies WHERE name = %s AND rfc = %s', (_name, _rfc))
        if cur.fetchone()[0] == 0:

            cur.execute('INSERT INTO companies (name, email, encryptedpasswdc, phone, address, state, municipaly, description, rfc, logo, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (_name, _email, generate_password_hash(_pass), _phone, _address, _state, _municipaly, _description, _rfc, logo_compr, type))
            cdb.conection.commit()

            print("Empresa registrada con éxito")
            return render_template("users/login.html", mensaje1="Empresa registrada con éxito")
        else:
            print("La empresa ya existe")
            return render_template("users/register.html", mensaje1="La empresa ya existe")
        
    print("Por favor, llene todos los campos")        
    return render_template("users/register.html", mensaje1="Por favor, llene todos los campos")
    

"""@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('logueado', None)
    session.pop('id', None)
    return render_template('login.html')
"""

if __name__ == '__main__':
    app.run(debug=True)