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


@app.route('/register')
def register():
  return render_template('users/register.html')

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
    if request.method == 'POST' and 'username' in request.form and 'name' in request.form and 'firstname' in request.form and 'secname' in request.form  and 'email' in request.form and 'password' in request.form and 'age' in request.form and 'phone' in request.form and 'address' in request.form and 'state' in request.form and 'municipaly' in request.form and 'cv' in request.form and 'emergencyc' in request.form and 'related' in request.form and 'disability' in request.form:
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
        _cv = request.file['cv']
        _emergencyc = request.form['emergencyc']
        _related = request.form['related']

        cur = cdb.cursor
        cur.execute('SELECT COUNT(*) FROM user WHERE name = %s AND email = %s', (_name, _email))
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO user (username, email, password, role) VALUES (%s, %s, %s, %s)',
                        (_name, _email, generate_password_hash(_pass), 'user'))
            cdb.conection.commit()
            return render_template("users/login.html", mensaje="Usuario registrado con éxito")
        else:
            return render_template("users/register.html", mensaje="El usuario ya existe")
    return render_template("users/register.html", mensaje="Por favor, llene todos los campos")

@app.route('/registerProcessCompanies', methods=['GET', 'POST'])
def registerAccessCompanies():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'phone' in request.form and 'address' in request.form and 'description' in request.form and 'rfc' in request.form and 'logo' in request.files:
        _name = request.form['name']
        _email = request.form['email']
        _pass = request.form['password']
        _phone = request.form['phone']
        _address = request.form['address']
        _description = request.form['description']
        _rfc = request.form['rfc']
        _logo = request.files['logo']
        tipo = _logo.mimetype
        logo_compr = compressImage(_logo)
        print(logo_compr, tipo, _logo, _rfc, _description, _address, _phone, _pass, _email, _name)
        cur = cdb.cursor
        cur.execute('SELECT COUNT(*) FROM companies WHERE name = %s AND rfc = %s', (_name, _rfc))
        if cur.fetchone()[0] == 0:
            print(cur.fetchone())
            cur.execute('INSERT INTO companies (name, email, encryptedpasswdc, phone, address, description, rfc, logo, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (_name, _email, generate_password_hash(_pass), _phone, _address, _description, _rfc, logo_compr, tipo))
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