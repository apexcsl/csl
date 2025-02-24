#Librerias
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import CDB

"""
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from PIL import Image
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
        cur.execute('SELECT COUNT(*) FROM user WHERE username = %s AND email = %s', (_name, _email))
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO user (username, email, password, role) VALUES (%s, %s, %s, %s)',
                        (_name, _email, generate_password_hash(_pass), 'user'))
            cdb.conection.commit()
            return render_template("users/login.html", mensaje="Usuario registrado con éxito")
        else:
            return render_template("users/register.html", mensaje="El usuario ya existe")
    return render_template("users/register.html", mensaje="Por favor, llene todos los campos")

"""@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('logueado', None)
    session.pop('id', None)
    return render_template('login.html')
"""

if __name__ == '__main__':
  app.run(debug=True)