from flask import Flask, render_template, url_for,request,session 
import random 
import smtplib


app = Flask(__name__)
app.secret_key = 'EmailVerification'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return '<script> alert("User not exists Please register"); window.location.href="/register";</script>'

@app.route('/register')
def register():   
    return render_template('register.html')




@app.route('/verify',methods=['POST'])
def verify():    
    otp = "".join([str(random.randint(0,9)) for i in range(4)])
    session['current_otp']=otp


    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('rainfallpproject@gmail.com','ikqqssrlvqnjutgu')


    username=request.form['email']
    email=request.form['email']
    password = request.form['password']
    session['user']=username
    session['email']=email
    session['password']=password


    message = "Your OTP for the site is : "+otp
    message = 'Subject: {}\n\n{}'.format("Rainfall Prediction", message)
    server.sendmail('rainfallpproject@gmail.com',email,message)    
    server.quit()
    return render_template('verify.html')

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']   
    otp = session['current_otp']
    
    if otp==(user_otp):
        return '<script> alert("Registration SUCCESSFULL login"); window.location.href="/login";</script>'
    return '<script> alert("Mismatchh OTP Try Again");</script>'+render_template('verify.html')


if __name__ == '__main__':
    app.run(debug=True)
