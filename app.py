from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
from resources.events import event
from resources.users import user
import models
import os

DEBUG = True
PORT = 8002

login_manager = LoginManager()

app = Flask(__name__)
CORS(app)

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
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(event, origins=['http://localhost:3000', 'http://https://local-la.herokuapp.com'],
supports_credentials=True)
app.register_blueprint(event, url_prefix='/api/v1/events')

CORS(user, origins=['http://localhost:3000', 'http://https://local-la.herokuapp.com'], 
supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)