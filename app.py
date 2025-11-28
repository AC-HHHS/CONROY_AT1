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

@app.route('/signUp')
def signUP():
    return render_template('signUp.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("SELECT * from USERS where email=? AND password=?",(email,password)).fetchall()
    if len(ans) > 0:
        connection.close()
        return render_template('login.html')
    else:
        cursor.execute("INSERT INTO USERS(first_name,last_name,email,password)values(?,?,?,?)",(first_name,last_name,email,password))
        connection.commit()
        connection.close()
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
