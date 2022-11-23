from flask import Flask, render_template, url_for,request,session , redirect
import random 
import smtplib
import db
import numpy as np
import pickle
import joblib
import time
import pandas
import os
import warnings
warnings.filterwarnings('ignore')




app = Flask(__name__)
app.secret_key = 'RainfallPrediction'
model = pickle.load(open("model\model.pkl", "rb"))
scaler = pickle.load(open("model\scaler.pkl", "rb"))






@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/prediction_Data')
def predictToday():
    return render_template('prediction_Data.html')

@app.route('/profile')
def profile():
    
    return render_template('profile.html',name = session['realname'],email = session['realemail'])

@app.route('/register')
def register():   
    return render_template('register.html')

@app.route('/forgetpassword')
def forgetpassword():   
    return render_template('forgetpassword.html')










@app.route('/verify',methods=['POST'])
def verify():    
    otp = "".join([str(random.randint(0,9)) for i in range(4)])
    session['current_otp']=otp


   


    name=request.form['name']
    email=request.form['email']
    password = request.form['password']
    session['user']=name
    session['email']=email
    session['password']=password

    datacheck = db.check_ifavailable(email)
    print(datacheck)

    if(datacheck==1):
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('rainfallpproject@gmail.com','ikqqssrlvqnjutgu')
        message = "Your OTP for the site is : "+otp
        message = 'Subject: {}\n\n{}'.format("Rainfall Prediction", message)
        server.sendmail('rainfallpproject@gmail.com',email,message)    
        server.quit()
        return render_template('verify.html')
    else:
        return '<script> alert("You are registering again so PLEASE LOGIN "); window.location.href="/login";</script>'
    


   

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']   
    otp = session['current_otp']
    
    if otp==(user_otp):
        db.insert_database(session['user'],session['email'],session['password'])
        return '<script> alert("Registration SUCCESSFULL login"); window.location.href="/login";</script>'
    return '<script> alert("Mismatchh OTP Try Again");</script>'+render_template('verify.html')


@app.route('/sendpassword',methods=['POST'] )
def sendpassword():  
    email=request.form['email']
    password = db.check_for_password(email)
    if(password==0):
        return '<script> alert("There is no such email registered \'SORRY\'"); window.location.href="/login";</script>'
    else:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('rainfallpproject@gmail.com','ikqqssrlvqnjutgu')
        message = "Your PASSWORD for the site is : "+password
        message = 'Subject: {}\n\n{}'.format("Rainfall Prediction(Forget Password", message)
        server.sendmail('rainfallpproject@gmail.com',email,message)    
        server.quit()
        return '<script> alert("Please Check your mail for Password"); window.location.href="/login";</script>'


@app.route('/userlogin',methods=['POST'])
def userlogin():
    email=request.form['email']
    password=request.form['password']   

    checkava = db.check_ifavailable(email)
    if(checkava==0):
        realpassword = db.check_for_password(email)
        if(realpassword==password):
            session['realemail'] = email
            session['realname'] = db.get_userame(email)             
            return '<script> window.location.href="/profile";</script>'
        else:
            return '<script> alert("Invalid Passsword"); window.location.href="/login";</script>'
    else:
        return '<script> alert("There is no such user Please check your email or Register"); window.location.href="/login";</script>'

@app.route('/predict', methods=["POST"])
def predict():
    column_names = ['MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed', 'WindSpeed9am',
       'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
       'Pressure3pm', 'Temp9am', 'Temp3pm', 'WindGustDir',
       'WindDir9am', 'WindDir3pm']
    
    feature_values = [int(request.values.get(name)) for name in column_names]
    print(f"input: {feature_values}")

    feature_values = [np.array(feature_values)]
    r=request.form['Rainfall']

    data = pandas.DataFrame(feature_values, columns=[column_names])
    data = scaler.fit_transform(data)
    data = pandas.DataFrame(data, columns=[column_names])
    prediction = model.predict(data)
    print(f"r: {r}")
    print(f"prediction: {prediction}")

    p=prediction[0]
    
    print(f"p: {p}")

    if ((r==1)):
        return render_template("resultYes.html")
    else:
        return render_template("resultNo.html")

    
    
    


if __name__ == '__main__':
    app.run(debug=True)
