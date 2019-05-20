import os
from modules import app

class Config:
    SECRET_KEY     = os.environ.get('SECRET_KEY')
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    MYSQL_HOST     = os.environ.get('MYSQL_HOST')

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['PER_PAGE'] = 3

# returns MySQL Username
def getMySQLUsername():
    return Config.MYSQL_USERNAME

# returns MySQL Password
def getMySQLPassword():
    return Config.MYSQL_PASSWORD

# returns MySQL Host
def getMySQLHost():
    return Config.MYSQL_HOST

# returns MySQL Database
def getMySQLDatabase():
    return Config.MYSQL_DATABASE


