from flask import jsonify, redirect, request, session, url_for
from flask import render_template
import re
from models.user import User

class UserController:

    __user = User()
    __status = ""

    def index(self):
        return render_template("index.html")

    def is_valid(self, email):
        check = False
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            check = True
        
        return check


    def submit_email(self):
        print(request.form['email'])
        email = request.form['email']
        self.__status = self.is_valid(email)

        if(request.method == "POST" and self.__status == False):
            self.__user.set_email(email)
            session['id'] = self.__user.get_id()
            print('session: ', session['id'])
            return jsonify({'status': self.__status})
        return redirect(url_for('index'))
        
