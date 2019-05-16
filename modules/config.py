import os
from modules import app

class Config:
    SECRET_KEY     = os.environ.get('SECRET_KEY')
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    MYSQL_HOST     = os.environ.get('MYSQL_HOST')

app.secret_key = Config.SECRET_KEY
