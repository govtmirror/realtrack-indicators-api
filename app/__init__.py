from flask import Flask
from flask.ext.uuid import FlaskUUID

app = Flask(__name__)
app.config.from_object('config')
FlaskUUID(app)

from app import views
