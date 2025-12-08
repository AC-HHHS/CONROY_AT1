from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os 
from question import questions
app = Flask(__name__)
app.secret_key = os.urandom(24)

questions = [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Rome"],
            "correct_answer_index": 1
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "correct_answer_index": 1
        }
    ]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation' , methods=['POST'])
def login_validation():
    middle_name = request.form.get('middle_name')
    email = request.form.get('email')
    fav_animal = request.form.get('fav_animal')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    user = cursor.execute("SELECT * FROM USERS WHERE middle_name=? and email=? and fav_animal=?",(middle_name,email,fav_animal)).fetchall()
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
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    fav_animal = request.form.get('fav_animal')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("SELECT * from USERS where middle_name=? AND email=? AND fav_animal=?",(middle_name,email,fav_animal)).fetchall()
    if len(ans) > 0:
        connection.close()
        return render_template('login.html')
    else:
        cursor.execute("INSERT INTO USERS(first_name,middle_name,last_name,email,password,fav_animal)values(?,?,?,?,?,?)",(first_name,middle_name,last_name,email,password,fav_animal))
        connection.commit()
        connection.close()
        return render_template('login.html')
    
@app.route('/faux')
def faux():
    return render_template('hint.html')

@app.route('/quoz')
def quiz():
        return redirect(url_for('bikeQuiz.html', questions=questions))

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
        score = 0
        user_answers = {}
        for i, question_data in enumerate(questions):
            selected_option = request.form.get(f'question_{i}')
            if selected_option is not None:
                user_answers[i] = int(selected_option)
                if int(selected_option) == question_data['correct_answer_index']:
                    score += 1
        return render_template('results.html', score=score, total_questions=len(questions), user_answers=user_answers, questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
