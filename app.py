#register as doctor - done
#register as user - done
#login - user/doctor - done
#contact admin for issues : done
#password hashing - done
#logout -done
#analysis of your heart:done
#register an appointment with a doctor - done
import os,hashlib
from flask import Flask,render_template,request,session,redirect,url_for
from flask_mysqldb import MySQL
import urllib.request
import re
import smtplib
from sendmail import sendmail
import MySQLdb.cursors
import numpy as np
import pandas as pd
import pickle
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'a'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = '...'
app.config['MYSQL_PASSWORD'] = '...'
app.config['MYSQL_DB'] = '...'
mysql = MySQL(app)

sc = pickle.load(open('sc.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))
@app.route('/')
def home():
    loggedin = getLoginDetails()
    return render_template('home.html',loggedin=loggedin)
@app.route('/check',methods=['GET','POST'])
def check():
    loggedin = getLoginDetails()
    if loggedin == False:
        return redirect(url_for('login'))
    return render_template('checkup.html',loggedin=loggedin)

@app.route('/docchat',methods=['GET','POST'])
def docchat():
    loggedin = getLoginDetails()
    if loggedin == False:
        return redirect(url_for('login'))
    return render_template('checkup.html',loggedin=loggedin)
    
@app.route('/predict',methods=['GET', 'POST'])
def predict():
    loggedin = getLoginDetails()
    if loggedin == False:
        return redirect(url_for('login'))
    age = request.form.get('age')
    sex = request.form.get('sex')
    lst = []
    cp = int(request.form.get('chest pain type (4 values)','0'))
    if cp == 0:
        lst += [1 , 0 ,0 ,0]
    elif cp == 1:
        lst += [0 ,1 ,0 ,0]
    elif cp == 2:
        lst += [0 ,0 ,1 ,0]
    elif cp >= 3:
        lst += [0 ,0 ,0 ,1]
    trestbps = int(request.form.get("resting blood pressure",'0' ))
    lst += [trestbps]
    chol = int(request.form.get("serum cholestoral in mg/dl",'0'))
    lst += [chol]
    fbs = int(request.form.get("fasting blood sugar > 120 mg/dl",'0'))
    if fbs == 0:
        lst += [1 , 0]
    else:
        lst += [0 , 1]
    restecg = int(request.form.get("resting electrocardiographic results (values 0,1,2)",'0'))
    if restecg == 0:
        lst += [1 ,0 ,0]
    elif restecg == 1:
        lst += [0 ,1 ,0]
    else:
        lst += [0 , 0,1]
    thalach = int(request.form.get("maximum heart rate achieved",'0'))
    lst += [thalach]
    exang = int(request.form.get("exercise induced angina",'0'))
    if exang == 0:
        lst += [1 , 0]
    else:
        lst += [0 ,1 ]
    final_features = np.array([lst])
    pred = model.predict( sc.transform(final_features))
    return render_template('result.html', prediction = pred,loggedin=loggedin)

@app.route('/regdoc',methods=['GET', 'POST'])
def regdoc():
    msg=''
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        hospital_name=request.form["hospital_name"]
        specialization_info=request.form["specialization_info"]
        country=request.form["country"]
        state=request.form["state"]
        hospital_address=request.form["hospital_address"]
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM doctorregister WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO doctorregister VALUES(NULL,% s,% s,% s,% s,% s,% s,% s,% s)',(username,email,hashlib.md5(password.encode()).hexdigest(),hospital_name,specialization_info,country,state,hospital_address))
            mysql.connection.commit()
            return redirect(url_for('login'))          
    return render_template('register_doc.html',msg=msg)


@app.route('/reguser',methods=['GET', 'POST'])
def reguser():
    msg=''
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM registeruser WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO registeruser VALUES(NULL,% s,% s,% s)',(username,email,hashlib.md5(password.encode()).hexdigest(),))
            mysql.connection.commit()
            return redirect(url_for('login'))
    return render_template('register_user.html',msg=msg)
@app.route('/login',methods=['GET', 'POST'])
def login():
    global user_id
    global doc_id
    msg=' '
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctorregister WHERE email = %s AND password = %s', (email, hashlib.md5(password.encode()).hexdigest(),))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM registeruser WHERE email = %s AND password = %s', (email,hashlib.md5(password.encode()).hexdigest(),))
        data = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['doc_id'] = account["doc_id"]
            id = account["doc_id"]
            session['email'] = account["email"]
            return redirect(url_for('home'))
        elif data:
            session['loggedin'] = True
            session['user_id'] = data["user_id"]
            id = data["user_id"]
            session['email'] = data["email"]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect email/password!'
    return render_template('login.html',msg=msg)

def getLoginDetails():
    cursor = mysql.connection.cursor()
    if 'email' not in session:
        loggedin = False
        username = ''
    else:
        loggedin = True
    return (loggedin)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('doc_id', None)
    session.pop('email', None)
    return render_template('home.html')

"""def IsActive():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM registeruser)"""
    
@app.route('/contact',methods=['GET','POST'])
def contact():
    msg=' '
    if request.method =="POST":
        email = request.form['email']
        subject= request.form['subject']
        Message = request.form['Message']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contact VALUES (NULL, % s, % s, % s)', (email,subject,Message))
        mysql.connection.commit()
        msg = 'You have successfully sent the message to admin !'
        TEXT = "from"+email+"Message:"+Message+"Subject:"+subject+" "
        sendmail(TEXT,#"enter your emailID"
        )
    return render_template('contact.html', msg = msg)


#to display all doctor details
@app.route('/connect',methods=['GET','POST'])  
def connect():
    loggedin = getLoginDetails()
    if loggedin == False:
        return redirect(url_for('login'))
  
  
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM doctorregister')
    account = cursor.fetchall()
    return render_template('connect.html',account=account,loggedin=loggedin)



if __name__== '__main__':
    app.run(host='localhost',debug = True,port = 8080)
 
