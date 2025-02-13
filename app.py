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

import base64
import hashlib
from config import config
"""

import pymysql
import re
import io

cdb = CDB()
cdb.connectDB()
conn = CDB()
conn.__init__()
user_name = "None"

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/home')
def home ():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('users/login.html')
"""
@app.route('/login', methods=['GET', 'POST'])
def loginAccess():
    global user_name, session, user
    if request.method == 'POST' and 'name' in request.form and 'password':
        _name = request.form['name']
        _pass = request.form['password']

        cur = cdb.cursor
        cur.execute('SELECT id, user, correo, contraseña_encriptada FROM usuario WHERE correo = %s', (_correo,))
        user = cur.fetchone()

        if user:
            id_user = user[0]
            user_name = user[1].split()[:2]  # Dividir el nombre en las primeras dos palabras
            correo_bd = user[2]
            contraseña_encriptada_bd = user[3]

            if _correo == "admin@gmail.com" and _contraseña == 'B!1w8NAt1T^%kvhUI*S^':
                session['logueado'] = True
                session['id'] = id_user
                return render_template("admin.html", user_name=user_name, session=session)
            else:
                if check_password_hash(contraseña_encriptada_bd, _contraseña):
                    session['logueado'] = True
                    session['id'] = id_user

                    return render_template("home.html", user_name=user_name, session=session)
                else:
                    return render_template("login.html", mensaje1="La contraseña no coincide")
        else:
            return render_template("login.html", mensaje1="Por favor, ingrese su correo y contraseña")
    return render_template("login.html", mensaje1="Por favor, ingrese su correo y contraseña")
"""

@app.route('/register')
def register():
  return render_template('users/register.html')

if __name__ == '__main__':
  app.run(debug=True)