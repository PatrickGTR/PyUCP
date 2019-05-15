from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'cnr'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Other
app.config['SECRET_KEY'] = 'secret_key_cnr_hello'

mysql.init_app(app)

from modules import routes



