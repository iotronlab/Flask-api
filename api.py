
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)

CORS(app)

app.config.from_pyfile('dbconfig.py')

db = SQLAlchemy(app)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins="*")


from websocket import *
from routes import *
from models import *
from auth import *


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)

