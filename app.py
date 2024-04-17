
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from multiprocessing import Process
from my_tracker import run_stock_tracker
import multiprocessing
from database import create_database
from send import send_email
import threading
import os




class UserInfo:
    def __init__(self, tracking_stocks, email_sms_value, timer, selected_option, name):
        self.tracking_stocks = tracking_stocks
        self.email_sms_value = email_sms_value
        self.timer = timer
        self.selected_option = selected_option
        self.name = name

   


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST']) #Home page
def index():
    global alert 
    global tracking_stocks
    global email_sms_value
    global timer
    global name
    global membership



    if request.method == 'POST': # if the inital website page retrives the data "POST METHOD" then the following request will grab the data, data being users info     
        data = request.form
        tracking_stocks = data.get('stocks', '')
        email_sms_value = data.get('email/sms', '')
        timer = data.get('timer', '')
        selected_option = request.form.get('membership')
        name = data.get('name', '')    

        print("Users name is: ", name)
        print("Stocks:", tracking_stocks)
        print("Email/SMS:", email_sms_value)
        print("Timer set to :", timer)
        
        print("Selected Option IS :", selected_option)
        alert= email_sms_value

       
        #Process(create_database, args=(UserInfo))

        # Run the stock tracker in a separate process
        Process(target=run_stock_tracker, args=(tracking_stocks, email_sms_value, timer, selected_option)).start() # Start the stock tracker
        

        Process(target= send_email, args=(email_sms_value, tracking_stocks, selected_option)).start() # Send the email

    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET',])    
def login():
    return render_template('login.html')
    
@app.route('/logout', methods = ['POST', 'GET',])
def logout():
    return render_template('logout.html')

@app.route('/sign-up', methods = [ 'POST' , 'GET'])
def sign_update():
    return render_template('sign-up.html')
@app.route('/politician', methods = ['POST','GET' ])
def get_politians():
    return render_template('politician.html') 

@app.route('/explanation', methods=['POST', 'GET'])
def explanation():
    return render_template('explanation.html')

@app.route('/own_pred', methods=['GET' ,'POST'])       
def own_pred():
    return render_template('own_pred.html')










if __name__ == "__main__":
    try:
        create_database(UserInfo)
        success = " DATABASE CREATED"
    except Exception as error:
        print (error)
        print ("database creation failed")    


    finally:
        app.run(debug=True)
    

