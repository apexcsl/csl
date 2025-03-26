from flask import Flask, render_template, request, redirect, url_for, session, send_file, g
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import CDB

import base64
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
app.config['PERMANENT_SESSION_LIFETIME'] = 900  
  



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
  cur = cdb.cursor
  cur.execute('SELECT AdminID, Username, Email FROM admins')
  admins = cur.fetchall()
  return render_template('admins/viewAdmins.html', admins=admins)

@app.route('/viewCompanies')
def viewCompanies():
    cur = cdb.cursor
    cur.execute('SELECT CompanyId, Name, Email, Phone, Address, State, Municipaly, Description, RFC, Logo, Type, uploaded_at FROM companies')
    companies = cur.fetchall()
    return render_template('applicants/viewCompanies.html', companies=companies)


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


def get_companies():
    cur = cdb.cursor
    cur.execute("SELECT companyid, name FROM companies")  
    opciones = cur.fetchall()
    return opciones


@app.route('/viewDisabilities')
def viewDisabilities():
    cur = cdb.cursor
    cur.execute('SELECT * FROM disabilities')
    disabilities = cur.fetchall()

    return render_template('admins/viewDisabilities.html', disabilities= disabilities)


@app.route('/editDisabilityForm/<int:disability_id>', methods=['GET', 'POST'])
def editDisabilityForm(disability_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM disabilities WHERE DisabilityId = %s', (disability_id,))
    disability = cur.fetchone()
    if disability:
        return render_template('admins/editDisability.html', disability=disability)
    else:
        return "Disability not found", 404
    
@app.route('/edit_disability/<int:disability_id>', methods=['GET', 'POST'])
def edit_disability(disability_id):
    cur = cdb.cursor
    if request.method == 'POST':
        _name = request.form['name']
        _category = request.form['category']
        _description = request.form['description']
        
        
        cur.execute('UPDATE disabilities SET name=%s, category=%s, description=%s WHERE DisabilityId=%s',
                    (_name, _category, _description ,disability_id))
        cdb.conection.commit()
        return redirect(url_for('viewDisabilities'))
    

@app.route('/delete_disability/<int:disability_id>', methods=['get'])
def delete_disability(disability_id):
    cur = cdb.cursor
    cur.execute('DELETE FROM disabilities WHERE DisabilityId = %s', (disability_id,))
    cdb.conection.commit()
    return redirect(url_for('viewDisabilities'))


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

@app.route('/details_company/<int:company_id>')
def details_company(company_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM companies WHERE CompanyId = %s', (company_id,))
    company = cur.fetchone()
    if company:
        imagen_base64 = base64.b64encode(company[10]).decode('utf-8')
        return render_template('applicants/detailsCompany.html', company=company, imagen_base64=imagen_base64)
    else:
        return "Company not found", 404


@app.route('/editCompanyForm/<int:company_id>', methods=['GET', 'POST'])
def editCompanyForm(company_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM companies WHERE CompanyId = %s', (company_id,))
    company = cur.fetchone()
    if company:
        imagen_base64 = base64.b64encode(company[10]).decode('utf-8')
        return render_template('admins/editCompany.html', company=company, imagen_base64=imagen_base64)
    else:
        return "Company not found", 404

@app.route('/edit_company/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    cur = cdb.cursor
    if request.method == 'POST':
        _name = request.form['name']
        _email = request.form['email']
        _phone = request.form['phone']
        _address = request.form['address']
        _state = request.form['state']
        _municipaly = request.form['municipality']
        _description = request.form['description']
        _rfc = request.form['rfc']
        
        cur.execute('UPDATE companies SET name=%s, email=%s, phone=%s, address=%s, state=%s, municipaly=%s, description=%s, rfc=%s WHERE CompanyId=%s',
                    (_name, _email, _phone, _address, _state, _municipaly, _description, _rfc, company_id))
        cdb.conection.commit()
        return redirect(url_for('viewCompanies'))
    
    cur.execute('SELECT * FROM companies WHERE CompanyId = %s', (company_id,))
    company = cur.fetchone()
    if company:
        return render_template('companies/editCompany.html', company=company)
    else:
        return "Company not found", 404

@app.route('/delete_company/<int:company_id>', methods=['get'])
def delete_company(company_id):
    cur = cdb.cursor
    cur.execute('DELETE FROM companies WHERE CompanyId = %s', (company_id,))
    cdb.conection.commit()
    return redirect(url_for('viewCompanies'))


@app.route('/editAdminForm/<int:admin_id>', methods=['GET', 'POST'])
def editAdminForm(admin_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM admins WHERE AdminId = %s', (admin_id,))
    admin = cur.fetchone()
    if admin:
        return render_template('admins/editAdmin.html', admin=admin)
    else:
        return "Admin not found", 404

@app.route('/edit_admin/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    cur = cdb.cursor
    if request.method == 'POST':
        _name = request.form['name']
        _email = request.form['email']
        
        cur.execute('UPDATE admins SET Username=%s, Email=%s WHERE AdminID=%s',
                    (_name, _email, admin_id))
        cdb.conection.commit()
        return redirect(url_for('viewAdmins'))
    
    cur.execute('SELECT * FROM admins WHERE AdminID = %s', (admin_id,))
    admin = cur.fetchone()
    if admin:
        return render_template('admins/editAdmin.html', admin=admin)
    else:
        return "Admin not found", 404

@app.route('/delete_admin/<int:admin_id>', methods=['get'])
def delete_admin(admin_id):
    cur = cdb.cursor
    cur.execute('DELETE FROM admins WHERE AdminID = %s', (admin_id,))
    cdb.conection.commit()
    return redirect(url_for('viewAdmins'))


@app.route('/viewApplicants')
def viewApplicants():
  cur = cdb.cursor
  cur.execute('SELECT ApplicantId, UserName, Name, FirstName, SecName, Email, Age, Phone, Address, State, Municipaly, Cv_Name, EmergencyContact, Related, DisabilityId FROM applicants')
  applicants = cur.fetchall()
  return render_template('admins/viewApplicants.html', applicants=applicants)

@app.route('/details_applicant/<int:applicant_id>')
def details_applicant(applicant_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM applicants WHERE ApplicantID = %s', (applicant_id,))
    applicant = cur.fetchone()
    cur.execute('SELECT * FROM disabilities WHERE DisabilityID = %s', (applicant[16],))
    disabilities = cur.fetchone() 
    if applicant:
        return render_template('applicants/detailsApplicant.html', applicant=applicant, disabilities=disabilities)
    else:
        return "Applicant not found", 404

@app.route('/editApplicantForm/<int:applicant_id>', methods=['GET', 'POST'])
def editApplicantForm(applicant_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM applicants WHERE ApplicantID = %s', (applicant_id,))
    applicant = cur.fetchone()
    disabilities = get_disabilities()
    if applicant:
        return render_template('applicants/editApplicant.html', applicant=applicant, disabilities=disabilities)
    else:
        return "Applicant not found", 404

@app.route('/edit_applicant/<int:applicant_id>', methods=['GET', 'POST'])
def edit_applicant(applicant_id):
    cur = cdb.cursor
    if request.method == 'POST':
        _username = request.form['username']
        _name = request.form['name']
        _firstname = request.form['firstname']
        _secname = request.form['secname']
        _email = request.form['email']
        _age = request.form['age']
        _phone = request.form['phone']
        _address = request.form['address']
        _state = request.form['state']
        _municipaly = request.form['municipality']
        _emergencyc = request.form['emergencyc']
        _related = request.form['related']
        _disabilityid = request.form['disability']
        
        cur.execute('UPDATE applicants SET username=%s, name=%s, firstname=%s, secname=%s, email=%s, age=%s, phone=%s, address=%s, state=%s, municipaly=%s, emergencyc=%s, related=%s, disabilityid=%s WHERE ApplicantID=%s',
                    (_username, _name, _firstname, _secname, _email, _age, _phone, _address, _state, _municipaly, _emergencyc, _related, _disabilityid, applicant_id))
        cdb.conection.commit()
        return redirect(url_for('viewApplicants'))
    
    cur.execute('SELECT * FROM appplicants WHERE ApplicantId = %s', (applicant_id,))
    applicant = cur.fetchone()
    if applicant:
        return render_template('applicants/editApplicant.html', applicant=applicant)
    else:
        return "Applicant not found", 404

@app.route('/delete_applicant/<int:applicant_id>', methods=['get'])
def delete_applicant(applicant_id):
    cur = cdb.cursor
    cur.execute('DELETE FROM applicants WHERE ApplicantID = %s', (applicant_id,))
    cdb.conection.commit()
    return redirect(url_for('viewApplicants'))


@app.route('/viewVacancies')
def viewVacancies():
    if session['role'] == 'company':
        cur = cdb.cursor
        cur.execute('SELECT * FROM vacancies WHERE CompanyID = %s', (session['id'],))
        vacancies = cur.fetchall()
        if not vacancies:
            return redirect(url_for('createVacancy'))
        else:
            cur.execute('SELECT * FROM companies WHERE CompanyID = %s', (vacancies[0][1],))
            company = cur.fetchone()
            cur.execute('SELECT * FROM disabilities WHERE DisabilityID = %s', (vacancies[0][2],))
            disabilities = cur.fetchone()
            return render_template('companies/viewVacancies.html', vacancies=vacancies, company=company, disabilities=disabilities)
        
    elif session['role'] == 'admin' or session['role'] == 'superadmin':
        cur = cdb.cursor
        cur.execute('SELECT * FROM vacancies')
        vacancies = cur.fetchall()
        if not vacancies:
            return redirect(url_for('createVacancy'))
        else:
            cur.execute('SELECT CompanyID, Name FROM companies')
            company = cur.fetchall()
            print(company)
            cur.execute('SELECT DisabilityID, Name FROM disabilities ')
            disabilities = cur.fetchall()
            print(disabilities)
            return render_template('companies/viewVacancies.html', vacancies=vacancies, companies=company, disabilities=disabilities)
        
    elif session['role'] == 'applicant':
        cur = cdb.cursor
        cur.execute('SELECT * FROM vacancies')
        vacancies = cur.fetchall()
        cur.execute('SELECT CompanyID, Name FROM companies')
        company = cur.fetchall()
        cur.execute('SELECT DisabilityID, Name FROM disabilities')
        disabilities = cur.fetchall()
        return render_template('companies/viewVacancies.html', vacancies=vacancies, companies=company, disabilities=disabilities)
    else:
        return redirect(url_for('login'))
    
@app.route('/createVacancy')
def createVacancy():
    companies = get_companies()
    disabilities = get_disabilities()
    return render_template('companies/createVacancy.html', companies=companies, disabilities=disabilities)

@app.route('/createVacancyProcess', methods=['GET', 'POST'])
def createVacancyProcess():
    try:
        if session['role'] == 'company':
            _companyid = session['id']
        elif session['role'] == 'admin':
            _companyid = request.form['company']
        else:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            _disabilityid = request.form['disability']
            _name = request.form['name']
            _description = request.form['description']
            _salary = request.form['salary']
            _state = request.form['state']
            _municipaly = request.form['municipality']
            _numbervacancy = request.form['numbervacancy']
            
            cur = cdb.cursor
            cur.execute('SELECT COUNT(*) FROM vacancies WHERE WorkPosition = %s AND CompanyID = %s', (_name, _companyid))
            if cur.fetchone()[0]==0:
                cur.execute('INSERT INTO vacancies (CompanyID, DisabilityID, Workposition, Description, Salary, State, Municipaly, NumberPosition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                            (_companyid, _disabilityid, _name, _description, _salary, _state, _municipaly, _numbervacancy))
                cdb.conection.commit()
                return redirect(url_for('viewVacancies'))
            else:
                print(cur.fetchone())
                print("La vacante ya existe")
                return render_template("companies/createVacancy.html", mensaje="La vacante ya existe")
        else:
            return render_template("companies/createVacancy.html", mensaje="Por favor, llene todos los campos")
    except Exception as e:
        print(e)

        
@app.route('/details_vacancies/<int:vacancy_id>')
def details_vacancies(vacancy_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM vacancies WHERE VacancyID = %s', (vacancy_id,))
    vacancies = cur.fetchone()
    cur.execute('SELECT * FROM companies WHERE CompanyID = %s', (vacancies[1],))
    companies = cur.fetchone() 
    cur.execute('SELECT * FROM disabilities WHERE DisabilityID = %s', (vacancies[2],))
    disabilities = cur.fetchone() 
    if vacancies:
        return render_template('companies/detailsVacant.html', vacancy=vacancies, companies=companies, disabilities=disabilities)
    else:
        return "Vacancies not found", 404

@app.route('/editVacancyForm/<int:vacancy_id>', methods=['GET', 'POST'])
def editVacantForm(vacancy_id):
    cur = cdb.cursor
    cur.execute('SELECT * FROM vacancies WHERE VacancyID = %s', (vacancy_id,))
    vacancies = cur.fetchone()
    cur.execute('SELECT * FROM companies WHERE CompanyID = %s', (vacancies[1],))
    companies = cur.fetchone() 
    disabilities = get_disabilities()

    if vacancies:
        return render_template('companies/editVacant.html', vacancy=vacancies, disabilities=disabilities, companies=companies)
    else:
        return "Vacancies not found", 404

@app.route('/edit_vacancy/<int:vacancy_id>', methods=['GET', 'POST'])
def edit_vacancy(vacancy_id):
    if session['role'] == 'company':
        _companyid = session['id']
    elif session['role'] == 'admin':
        _companyid = request.form['company']
    else:
        return redirect(url_for('login'))
    cur = cdb.cursor
    if request.method == 'POST':
        _workposition = request.form['name']
        _description = request.form['description']
        _salary = request.form['salary']
        _disabilityid = request.form['disability_id']
        _numberposition = request.form['numberp']
        _state = request.form['state']
        _municipaly = request.form['municipality']
        
        cur.execute('UPDATE vacancies SET Workposition=%s, Description=%s, Salary=%s, CompanyID=%s, DisabilityID=%s, NumberPosition=%s, State=%s, Municipaly=%s  WHERE VacancyID=%s',
                    (_workposition, _description, _salary, _companyid, _disabilityid, _numberposition, _state, _municipaly, vacancy_id))
        cdb.conection.commit()
        return redirect(url_for('viewVacancies'))
    
    cur.execute('SELECT * FROM vacancies WHERE VacancyId = %s', (vacancy_id,))
    vacancies = cur.fetchone()
    if vacancies:
        return render_template('companies/editVacant.html', vacancies=vacancies)
    else:
        return "Vacancies not found", 404

@app.route('/delete_vacancy/<int:vacancy_id>', methods=['get'])
def delete_vacancy(vacancy_id):
    cur = cdb.cursor
    cur.execute('DELETE FROM vacancies WHERE VacancyID = %s', (vacancy_id,))
    cdb.conection.commit()
    return redirect(url_for('viewVacancies'))

@app.route('/viewApplicantsVacancy/<int:vacancy_id>', methods=['GET'])
def viewApplicantsVacancy(vacancy_id):
    cur =cdb.cursor
    cur.execute('SELECT ApplicantID, Name, Age, Email, Phone FROM Applicants WHERE ApplicantID IN (SELECT ApplicantID FROM Applications WHERE VacancyId = %s)', vacancy_id)
    applicants=cur.fetchall()
    return render_template('companies/viewApplicantsCompanies.html', vacancy_id=vacancy_id, applicants=applicants)

@app.route('/acceptApplicant/<int:Vacancy_id>, <int:Applicant_id>')
def acceptApplicant(vacancy_id, applicant_id):
    cur=cdb.cursor
    cur.execute('INSERT INTO Approved (VacancyID, ApplicantID) VALUES (%s, %s)', vacancy_id, applicant_id)
    cur.connection.commit()
    return render_template('/home')

@app.route('/rejectApplicant/<int:Vacancy_id>, <int:Applicant_id>')
def rejectApplicant(vacancy_id, applicant_id):
    cur = cdb.cursor
    cur.execute('DELETE FROM Applications WHERE VacancyID = %s AND ApplicantID = %s', vacancy_id, applicant_id)
    cur.connection.commit()
    return render_template('/home')

@app.route('/RedirectApplicant', methods=['POST'])
def redirectApplicant():
    destinationVacancy=request.json
    vacancy=destinationVacancy.get("DestinationVacancy")
    id_Aplicant = request.args.get("id_aplicant")
    id_vacancy = request.args.get("id_vacancy")
    cur = cdb.cursor
    cur.execute('SELECT ID VacancyID From Vacancies where Name = %s AND CompanyID = %s', (vacancy, session[id]))
    cur.fetchone()
    cur.execute('INSERT INTO Applications (ApplicantID, VacancyID, ) VALUES (%s, %s)' (id_Aplicant, destinationVacancy))
    cur.connection.commit()
    cur.execute('DELETE FROM Applications WHERE VacancyId = %s' (id_vacancy))
    cur.connection.commit()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)