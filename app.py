from flask import Flask, render_template, request, redirect
import sqlite3
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation' , methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    user = cursor.execute("SELECT * FROM USERS WHERE email=? and password=?",(email,password)).fetchall()
    if len(user) > 0 :
        return redirect(f'/home?first_name={user[0][0]}&last_name={user[0][1]}&email={user[0][2]}')
    else:
        return redirect('/')
    
@app.route('/home')
def home():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')

    return render_template('userHome.html', first_name=first_name, last_name=last_name, email=email)

if __name__ == '__main__':
    app.run(debug=True)
