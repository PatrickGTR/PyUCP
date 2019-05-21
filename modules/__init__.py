from flask import Flask
from modules.config import Config


app = Flask(__name__)
app.config.from_object(Config)

from modules import routes




