
import json
from flask import redirect,  url_for
from flask import jsonify, request, session
from datetime import datetime
from models.rate import Rate

class RateController:
    
    def rate(self):
        if request.method == "POST":
            user_id= session['id']
            rate = request.get_json().get('r')
            print("rate", rate)
             # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", date_time)	    

            __rate = Rate(user_id, rate, date_time)
            return jsonify({'response': ""})
        return redirect(url_for('index'))
