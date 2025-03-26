# Librerias necesarias para la conexion a la base de datos
import re
import pymysql
from werkzeug.security import generate_password_hash

# Clase para creacion y/o conexion a la base de datos
class CDB():

    # Funcion para inicializar la clase
    def __init__(self):
        self.puertoXampp, self.usuarioXampp = self.detectarPuertoXampp()
        try:
            self.conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=int(self.puertoXampp), db="apex_test")
            self.cursor = self.conection.cursor()
            print("\nConexión exitosa\n")

        except pymysql.Error as err:
            self.conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=int(self.puertoXampp))
            self.cursor = self.conection.cursor()
            self.cursor.execute("CREATE DATABASE if not exists apex_test")
            self.cursor.execute("USE apex_test")
            print("\nCreación exitosa\n")
    
    # Funcion para detectar la informacion del usuario de xampp
    @staticmethod
    def detectarPuertoXampp(rutaXampp='C:/xampp/mysql/bin/my.ini'):
        try:
            with open(rutaXampp, 'r') as archivo:
                contenido = archivo.read()

                # Buscamos el puerto
                puerto = re.search(r'port[ ]*=[ ]*(\d+)', contenido)
                if puerto:
                    puerto = puerto.group(1)
                else:
                    print("No se encontró el puerto")
                    puerto = None

                # Buscamos el usuario
                usuario = re.search(r'user[ ]*=[ ]*(\w+)', contenido)
                if usuario:
                    usuario = usuario.group(1)
                else:
                    print("No se encontró el usuario")
                    usuario = "root"
                return puerto, usuario
        
        # Por si no se encuentra el archivo de xampp
        except FileNotFoundError:
            print("No se encontró el archivo")
            return None, None
    
    # Especificar el puerto y usuario de xampp
    puertoXampp, usuarioXampp = detectarPuertoXampp()
    if puertoXampp:
        print(f"\nEl puerto de MySQL es: {puertoXampp}")
        print(f"El usuario de MySQL es: {usuarioXampp}")
    else:
        print(f"\nNo se encontró la información")

    # Funcion para crear la tabla Admins
    def createTableAdmins(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Admins (AdminID INT AUTO_INCREMENT PRIMARY KEY, Username VARCHAR(255), Email VARCHAR(255), EncryptedPassword VARCHAR(255), profilePhoto LONGBLOB, Type VARCHAR(50), uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")
     
    # Funcion para crear la tabla Applicants
    def createTableApplicants(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Applicants (ApplicantID INT AUTO_INCREMENT PRIMARY KEY, UserName VARCHAR(255), Name VARCHAR(255), Firstname VARCHAR(255), Secname VARCHAR(255), Email VARCHAR(255), EncryptedPasswdA VARCHAR(255), profilePhoto LONGBLOB, Type VARCHAR(50), Age INT, Phone VARCHAR(255), Address VARCHAR(255), State VARCHAR(255), Municipaly VARCHAR(255), Cv_Name VARCHAR(255), Cv_Data  LONGBLOB, EmergencyContact VARCHAR(255), Related VARCHAR(255), DisabilityID INT,  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    # Funcion para crear la tabla Companies
    def createTableCompanies(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Companies (CompanyID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Email VARCHAR(255), EncryptedPasswdC VARCHAR(255), Phone VARCHAR(255), Address VARCHAR(255), State VARCHAR(255), Municipaly VARCHAR(255), Description VARCHAR(255), RFC VARCHAR(255), profilePhoto LONGBLOB, Type VARCHAR(50), uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    # Funcion para crear la tabla Disabilities
    def createTableDisabilities(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Disabilities (DisabilityID INT AUTO_INCREMENT PRIMARY KEY, Category VARCHAR(255), Name VARCHAR(255), Description VARCHAR(255))")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    #Funcion para crear la tabla Vacantes
    def createTableVacancies(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Vacancies (VacancyID INT AUTO_INCREMENT PRIMARY KEY, CompanyID INT, DisabilityID INT, ApplicantID INT, Workposition VARCHAR(255), Description VARCHAR(255), Salary VARCHAR(255), State VARCHAR(255), Municipaly VARCHAR(255), NumberPosition INT, Type VARCHAR(255), uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    # Funcion para crear la tabla Videos
    def createTableVideos(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Videos (VideoID INT AUTO_INCREMENT PRIMARY KEY, CompanyID INT, Name VARCHAR(255), Description VARCHAR(255), Video VARCHAR(255), uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    # Funcion para crear la tabla Messages
    def createTableMessages(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Messages (MessageID INT AUTO_INCREMENT PRIMARY KEY, SenderUserName VARCHAR(255), RecipientUserName VARCHAR(255), Message TEXT, Status VARCHAR(255), uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla mensajes creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")


    # Funcion para crear la tabla Aprobados
    def createTableApproved(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Approved (ApprovedID INT AUTO_INCREMENT PRIMARY KEY, CompanyID INT, DisavilityID INT, ApplicantID INT, uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla user: {err}")

    #Función para crear la tabla Aplications
    def createTableApplications(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Applications (AppID Int AUTO_INCREMENT PRIMARY KEY, VacancyID INT, ApplicantID INT, uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("\nTabla Applications creada con éxito")
        except pymysql.Error as err:
            print(f"\nError al crear la tabla Applications: {err}")


    #Funcion para insertar discapacidades
    def insertDisability(self, category, name, description):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Disabilities WHERE Category = %s AND Name = %s", (category, name))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("INSERT INTO Disabilities (Category, Name, Description) VALUES (%s, %s, %s)", (category, name, description))
                self.conection.commit()
                print("Discapacidades insertada con éxito")
            else:
                print("La discapacidad ya existe")
        except pymysql.Error as err:
            print(f"\nError al insertar la discapacidad: {err}")

    # Funcion al conectar a la base de datos
    def connectDB(self):
        try:
            self.createTableAdmins()
            self.createTableApplicants()
            self.createTableCompanies()
            self.createTableDisabilities()
            self.createTableVacancies()
            self.createTableVideos()
            self.createTableMessages()
            self.createTableApproved()
            self.createTableApplications()
            datos = [
                ('Fisica o Motora', 'Parálisis', 'Pérdida completa o parcial de la capacidad de movimiento de una o más partes del cuerpo debido a daño en el sistema nervioso o muscular.'),
                ('Fisica o Motora', 'Amputaciones', 'Pérdida de una extremidad o parte del cuerpo, que afecta la movilidad y el uso de prótesis o adaptaciones.'),
                ('Fisica O Motora', 'Distrofias musculares', 'Trastornos genéticos progresivos que debilitan los músculos y afectan la capacidad motora de la persona.'),
                ('Fisica o Motora', 'Escleorosis múltiple', 'Enfermedad autoinmune crónica que afecta el sistema nervioso central y causa problemas de movilidad, fatiga y coordinación.'),
                ('Fisica o Motora', 'Lesiones en la médula espinal', 'Daño a la médula espinal que provoca pérdida de función motora y sensorial, incluyendo parálisis en diversas partes del cuerpo.'),
                ('Sensorial', 'Visual', 'Afecta la capacidad de ver, desde baja visión hasta ceguera total, limitando la percepción visual y la orientación en el entorno.'),
                ('Sensorial', 'Auditiva', 'Pérdida parcial o total de la audición, que puede interferir en la comunicación verbal y la percepción de sonidos del entorno.'),
                ('Intelectual', 'Discapacidad Intelectual', 'Limitaciones significativas en el funcionamiento intelectual y en las habilidades adaptativas, lo que afecta el aprendizaje y la autonomía.'),
                ('Psíquica o Mental', 'Transtornos de ansiedad', 'Condiciones mentales caracterizadas por miedo, nerviosismo o preocupación excesiva, que interfieren con la vida diaria.'),
                ('Psíquica o Mental', 'Depresión cronica severa', 'Trastorno mental que causa un estado de ánimo persistente de tristeza, desesperanza, y pérdida de interés en actividades.'),
                ('Psíquica o Mental', 'Esquizofrenia', 'Trastorno mental grave que afecta la capacidad de pensar, sentir y comportarse con claridad, causando alucinaciones y delirios.'),
                ('Psíquica o Mental', 'Transtornos de personalidad', 'Patrones de comportamiento rígidos y disfuncionales que afectan las relaciones sociales y la percepción de uno mismo')]
            for category, name, description in datos:
                self.insertDisability(category, name, description)
        except pymysql.Error as err:
            print(f"\nError al conectar a la base de datos: {err}")

    # Funcion para cerrar la conexion
    def closeDB(self):
        self.cursor.close()
        self.conection.close()
        print("\nConexión cerrada con éxito\n")

