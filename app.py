from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
from resources.events import event
from resources.users import user
import models

DEBUG = True
PORT = 8002

login_manager = LoginManager()

app = Flask(__name__)
CORS(app)
app.secret_key = "secret key"
login_manager.init_app(app)

CORS(event, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(event, url_prefix='/api/v1/events')
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

@login_manager.user_loader 
def load_user(userId):
    try:
        return models.User.get(models.User.id == userId)
    except models.DoesNotExist:
        return None

app.secret_key = "thissisthesecretkey"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userId):
    try:
        return models.User.get(models.User.id == userId)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response): 
    """Close the database"""
    g.db.close()
    return response

CORS(event, origins=['http://localhost:3000'],
supports_credentials=True)

app.register_blueprint(event, url_prefix='/api/v1/events')

CORS(user, origins=['http://localhost:3000'],
supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
 
    CORS(event, origins=['http://localhost:3000'], supports_credentials=True) 
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
