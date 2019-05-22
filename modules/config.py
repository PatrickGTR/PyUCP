import os

class Config:
    PER_PAGE        = 3
    SECRET_KEY      = os.environ.get('SECRET_KEY')
    
    MYSQL_USERNAME  = os.environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD  = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE  = os.environ.get('MYSQL_DATABASE')
    MYSQL_HOST      = os.environ.get('MYSQL_HOST')


