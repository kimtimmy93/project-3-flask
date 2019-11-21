from flask import Flask, g
from flask_cors import CORS
from resources.events import event

import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(event, origins=['http://localhost:3000'], supports_credentials=True) # adding this line
# CORS(user, origins=['http://localhost:3000'], supports_credentials=True) # adding this line
#support credentials allows cookies to be sent to our api session

app.register_blueprint(event, url_prefix='/api/v1/events/');
# app.register_blueprint(user, url_prefix='/api/v1/user/');
 # adding this line








# The default URL ends in / ("my-website.com/").


# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)