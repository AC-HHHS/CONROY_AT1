from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os 
from question import questions

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation' , methods=['POST'])
def login_validation():
    email = request.form.get('email')
    fav_animal = request.form.get('fav_animal')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    user = cursor.execute("SELECT * FROM USERS WHERE email=? and fav_animal=?",(email,fav_animal)).fetchall()
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
    fav_animal = request.form.get('fav_animal')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("SELECT * from USERS where email=? AND fav_animal=?",(email,fav_animal)).fetchall()
    if len(ans) > 0:
        connection.close()
        return render_template('login.html')
    else:
        cursor.execute("INSERT INTO USERS(first_name,last_name,email,password,fav_animal)values(?,?,?,?,?)",(first_name,last_name,email,password,fav_animal))
        connection.commit()
        connection.close()
        return render_template('login.html')


@app.route('/quoz')
def quoz():
    return render_template('bikeQuiz.html')
   
@app.route('/quozing')
def index():
    session['score'] = 0
    session['current_question_index'] = 0 

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    current_question_index = session.get('current_question_index', 0)

    if current_question_index >= len(questions):
        return redirect(url_for('results'))
    
    question_data = questions[current_question_index]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer == question_data['correct_answer']:
            session['score'] += 1
        session['current_question_index'] += 1
        return render_template('bikeQuiz.html', question=question_data, question_number=current_question_index + 1)
    
@app.route('/results')
def results():
    score = session.get('score', 0)
    total_questions = len(questions)
    return render_template('results.html', score=score, toatl=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
