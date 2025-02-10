from flask import Flask, render_template, request
import pymysql

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

        cur = cbd.cursor
        cur.execute('SELECT id, nombrec, correo, contraseña_encriptada FROM usuario WHERE correo = %s', (_correo,))
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