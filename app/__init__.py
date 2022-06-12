from flask_socketio import SocketIO
from flask import Flask
import gevent, geventwebsocket
from flask_sqlalchemy import SQLAlchemy

# Initialise app and config

app = Flask(__name__)
app.config["SECRET_KEY"] = "burgerio"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init other modules made by the app

socketio = SocketIO(app=app)
db = SQLAlchemy()
db.init_app(app)


# Connect the routes
from app import routes