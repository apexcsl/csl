#Librerias
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import CDB

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

from mediaUploader import *

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


@app.route('/loginProcess', methods=['GET', 'POST'])
def loginAccess():
    global user_name, session, user

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        _email = request.form['email']
        _pass = request.form['password']


        cur = cdb.cursor

        
        if _email == "apexcsl@gmail.com" and _pass == 'B!1w8NAt1T^%kvhUI*S^':
            session['id'] = 0
            session['role'] = 'superadmin'
            user_name = ['Admin', 'Principal']
            return render_template("home.html", user_name=user_name, session=session)

        cur.execute('SELECT AdminId, UserName, EncryptedPassword FROM admins WHERE email = %s', (_email,))
        admin = cur.fetchone()
        print(session)
        if admin:
            if check_password_hash(admin[2], _pass):
                session['id'] = admin[0]
                session['role'] = 'admin'
                user_name = [admin[1]]
                return render_template("home.html", user_name=user_name, session=session)
            else:
                return render_template("users/login.html", mensaje1="Contraseña incorrecta")

        cur.execute('SELECT CompanyId, name, EncryptedPasswdC FROM companies WHERE email = %s', (_email,))
        company = cur.fetchone()
        print(session)
        if company != None:
            print("entre aqui al company")
            if check_password_hash(company[2], _pass):
                session['id'] = company[0]
                session['role'] = 'company'
                user_name = [company[1]]
                return render_template("home.html", user_name=user_name, session=session)
            else:
                return render_template("users/login.html", mensaje1="Contraseña incorrecta")

        print(session)
        cur.execute('SELECT ApplicantId, UserName, EncryptedPasswdA, name FROM applicants WHERE email = %s', (_email,))
        applicant = cur.fetchone()
        print(applicant)
        print(applicant[2])
        if applicant:
            print("entre aqui al applicant")
            if check_password_hash(applicant[2], _pass):
                session['id'] = applicant[0]
                session['role'] = 'applicant'
                user_name = [applicant[3]]
                return render_template("home.html", user_name=user_name, session=session)
            else:
                return render_template("users/login.html", mensaje1="Contraseña incorrecta")

        return render_template("users/login.html", mensaje1="Usuario no encontrado")

    return render_template("users/login.html", mensaje1="Ingrese su correo y contraseña")


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
        if verifyRegisterData(_email):
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
        cv = request.files['cv']
        _emergencyc = request.form['emergencyc']
        _related = request.form['related']
        _disabilityid = request.form['disability']
        
        _cv_data = compressPdf(cv)

        cur = cdb.cursor
        if verifyRegisterData(_email):
            cur.execute('INSERT INTO applicants (username, name, firstname, secname, email, encryptedpasswda, age, phone, address, state, municipaly, Cv_Name, Cv_Data, emergencycontact, related, disabilityid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (_username, _name, _secname, _firstname, _email, generate_password_hash(_pass), _age, _phone, _address, _state, _municipaly, cv.filename, _cv_data, _emergencyc, _related, _disabilityid))
            
            """cur.execute('INSERT INTO applicants (username, name, firstname, secname, email, encryptedpasswda, age, phone, address, state, municipaly, emergencycontact, related, disabilityid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (_username, _name, _firstname, _secname,  _email, generate_password_hash(_pass), _age, _phone, _address, _state, _municipaly, _emergencyc, _related, _disabilityid))"""
            
            cdb.conection.commit()
            return render_template("users/login.html", mensaje="Usuario registrado con éxito")
        else:
            print("El usuario ya existe")
            return render_template("users/register.html", mensaje="El usuario ya existe")
    print("Por favor, llene todos los campos")
    return render_template("users/register.html", mensaje="Por favor, llene todos los campos")




@app.route('/registerProcessCompanies', methods=['GET', 'POST'])
def registerAccessCompanies():
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
        if verifyRegisterData(_email, _rfc):

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
    


def verifyRegisterData(email, rfc=None):
    cur = cdb.cursor

    if rfc:
        cur.execute('SELECT COUNT(*) FROM companies WHERE email = %s OR rfc = %s', (email, rfc))
        if cur.fetchone()[0] > 0:
            print("El correo o RFC ya están registrados en empresas.")
            return False


    cur.execute('SELECT COUNT(*) FROM admins WHERE email = %s', (email,))
    if cur.fetchone()[0] > 0:
        print("El correo ya está registrado en administradores.")
        return False


    cur.execute('SELECT COUNT(*) FROM applicants WHERE email = %s', (email,))
    if cur.fetchone()[0] > 0:
        print("El correo ya está registrado en aplicantes.")
        return False

    return True

@app.route('/download_pdf/<int:file_id>')
def download_pdf(file_id):

    cur = cdb.cursor
    cur.execute("SELECT Cv_Name, Cv_Data FROM applicants WHERE ApplicantId=%s", (file_id,))
    file = cur.fetchone()

    if not file:
        return "File not found", 404

    filename, filedata= file

    original_pdf = decompressPdf(filedata)

    return send_file(
        io.BytesIO(original_pdf),
        download_name=filename,
        as_attachment=True
    )

    

"""@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('logueado', None)
    session.pop('id', None)
    return render_template('login.html')
"""

if __name__ == '__main__':
    app.run(debug=True)