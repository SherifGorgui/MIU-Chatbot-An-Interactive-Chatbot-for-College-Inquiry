from flask import Flask
# from flask_ngrok import run_with_ngrok
from controllers.qa_controller import QAController
qaController = QAController()

from controllers.user_controller import UserController
userController = UserController()

from controllers.rate_controller import RateController
rateController = RateController()

import os
# initialize flask app
app = Flask(__name__)
# run_with_ngrok(app)

app.secret_key = os.urandom(24) # to use sessions secret key is a must

@app.route('/')
def index():
    return userController.index()

@app.route('/submit_email', methods=['GET', 'POST'])
def submit_email():
    return userController.submit_email();

@app.route('/request', methods=['GET', 'POST'])
def send_msg():
    return qaController.send_msg()

@app.route('/rate', methods= ['GET', 'POST'])
def rate():
    return rateController.rate()

if __name__ == "__main__":
    app.run()
