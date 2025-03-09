class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'
    MAIL_SERVER = 'smtp.gmail.com' 
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'apexcsl155@gmail.com'
    MAIL_PASSWORD = 'hcjb bnvm peib tguj'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'login'

config = {
    'development': DevelopmentConfig
}

### APP PASSWORD EMAIL SENDER 2FA ###
"""hcjb bnvm peib tguj"""

### TWILIO ###
"""XMUBFTJXNULPKSPA1V5A9WPB"""