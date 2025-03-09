from flask import Flask, render_template, request, redirect, url_for, session, send_file, g
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import CDB

from config import config
from mediaUploader import *

cdb = CDB()
cdb.connectDB()
conn = CDB()
conn.__init__()
user_name = "None"

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = True     
app.config['SESSION_USE_SIGNER'] = True    
app.config['PERMANENT_SESSION_LIFETIME'] = 259200  
  



@app.route('/')
def index():
  return render_template('home.html')

@app.route('/home')
def home ():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('users/login.html')

@app.route('/viewAdmins')
def viewAdmins():
  return render_template('admins/viewAdmins.html')

@app.route('/viewCompanies')
def viewCompanies():
  return render_template('applicants/viewCompanies.html')

@app.route('/viewApplicants')
def viewApplicants():
  return render_template('admins/viewApplicants.html')

@app.route('/viewVacancies')
def viewVacancies():
  return render_template('companies/viewVacancies.html')

@app.route('/viewVideos')
def viewVideos():
  return render_template('companies/viewVideos.html')


@app.route('/loginProcess', methods=['POST'])
def loginAccess():
    if 'email' in request.form and 'password' in request.form:
        _email = request.form['email']
        _pass = request.form['password']
        cur = cdb.cursor

        # Superadmin Hardcodeado
        if _email == "apexcsl@gmail.com" and _pass == 'B!1w8NAt1T^%kvhUI*S^':
            session['id'] = 0
            session['role'] = 'superadmin'
            session['user_name'] = 'Admin Principal'
            session.permanent = True
            return redirect(url_for('index'))

        # Verificar usuario en DB
        cur.execute('SELECT AdminId, UserName, EncryptedPassword FROM admins WHERE email = %s', (_email,))
        admin = cur.fetchone()
        
        if admin and check_password_hash(admin[2], _pass):
            session['id'] = admin[0]
            session['role'] = 'admin'
            session['user_name'] = admin[1]
            session.permanent = True
            return redirect(url_for('index'))
        
        cur.execute('SELECT CompanyId, name, EncryptedPasswdC FROM companies WHERE email = %s', (_email,))
        company = cur.fetchone()
        
        if company and check_password_hash(company[2], _pass):
            session['id'] = company[0]
            session['role'] = 'company'
            session['user_name'] = company[1]
            session.permanent = True
            return redirect(url_for('index'))
        
        cur.execute('SELECT ApplicantId, UserName, EncryptedPasswdA, name FROM applicants WHERE email = %s', (_email,))
        applicant = cur.fetchone()
        
        if applicant and check_password_hash(applicant[2], _pass):
            session['id'] = applicant[0]
            session['role'] = 'applicant'
            session['user_name'] = applicant[3]
            session.permanent = True
            return redirect(url_for('index'))
        
        return render_template("users/login.html", mensaje1="Usuario o contraseña incorrectos")



@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login'))


def get_disabilities():
    cur = cdb.cursor
    cur.execute("SELECT disabilityid, name FROM disabilities")  
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


@app.route('/myProfile')
def myProfile():
    if session['role'] == 'company':
        cur = cdb.cursor
        cur.execute('SELECT * FROM companies WHERE CompanyId = %s', (session['id'],))
        company = cur.fetchone()
        return render_template('users/companyProfile.html', company=company)
    elif session['role'] == 'applicant':
        cur = cdb.cursor
        cur.execute('SELECT * FROM applicants WHERE ApplicantId = %s', (session['id'],))
        applicant = cur.fetchone()
        return render_template('users/applicantProfile.html', applicant=applicant)
    elif session['role'] == 'admin':
        cur = cdb.cursor
        cur.execute('SELECT * FROM admins WHERE AdminId = %s', (session['id'],))
        admin = cur.fetchone()
        return render_template('users/adminProfile.html', admin=admin)
    else:
        return redirect(url_for('login'))

@app.before_request
def load_session():
    g.user = session.get('user_name')




"""@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('logueado', None)
    session.pop('id', None)
    return render_template('login.html')
"""

if __name__ == '__main__':
    app.run(debug=True)