from flask import Flask

app = Flask(__name__)

# Other
app.config['SECRET_KEY'] = 'secret_key_cnr_hello'

from modules import routes


