#Librerias necesarias para la conexion a la base de datos
import re
import pymysql

#Clase para creacion y/o conexion a la base de datos
class CDB():

    #Funcion para inicializar la clase
    def __init__(self):
        try:
            self.conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=self.puertoXampp, db="apex_test")
            self.cursor = self.conection.cursor()
            print("\nConexión exitosa\n")

        except pymysql.Error as err:
            self.conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=self.puertoXampp)
            self.cursor = self.conection.cursor()
            self.cursor.execute("CREATE DATABASE if not exists apex_test")
            self.cursor.execute("USE apex_test")
            print("\nCreación exitosa\n")
    
    #Duncion para detectar la informacion del usuario de xampp
    def detectarPuertoXampp(self, rutaXampp='C:/xampp/mysql/bin/my.ini'):
        try:
            with open(rutaXampp, 'r') as archivo:
                contenido = archivo.read()

                #Buscamos el puerto
                puerto = re.search(r'port=(\d+)', contenido)
                if puerto:
                    return puerto.group(1)
                else:
                    print("No se encontró el puerto")
                    puerto = None

                #Buscamos el usuario
                usuario = re.search(r'user=(\w+)', contenido)
                if usuario:
                    return usuario.group(1)
                else:
                    print("No se encontró el usuario")
                    usuario = "root"

                return puerto, usuario
        
        #Por si no se encuentra el archivo de xampp
        except FileNotFoundError:
            print("No se encontró el archivo")
            return None, None
    
    #Especificar el puerto y usuario de xampp
    puertoXampp, usuarioXampp = detectarPuertoXampp()
    if puertoXampp:
        print(f"\nEl puerto de MySQL es: {puertoXampp}")
        print(f"\nEl usuario de MySQL es: {usuarioXampp}")
    else:
        print(f"\nNo se encontró la información")

    #Funcion para crear la tabla usuarios
    def createTableUser(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), email VARCHAR(255), password VARCHAR(255), role VARCHAR(255))")
            print("\nTabla creada con éxito\n")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    #Funcion para insertar un usuario predeterminado
    def insertUser(self, username, email, password, role):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM user WHERE username = %s AND email = %s", ('May', 'mayrinreyes1707@gmail.com'))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("INSERT INTO user (username, email, password, role) VALUES (%s, %s, %s, %s)", ('May', 'mayrinreyes1707@gmail.com', 'Kirbytest', 'admin'))
            else:
                print("\nEl usuario ya existe\n")
            self.conection.commit()
            print("\nUsuario insertado con éxito\n")
        except pymysql.Error as err:
            print(f"\nError al insertar el usuario: {err}")

    #Funcion al conectar a la base de datos
    def connectDB(self):
        try:
            self.createTableUser()
            self.insertUser()
        except pymysql.Error as err:
            print(f"\nError al conectar a la base de datos: {err}")

    #Funcion para cerrar la conexion
    def closeDB(self):
        self.cursor.close()
        self.conection.close()
        print("\nConexión cerrada con éxito\n")

