from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from question import questions

app = Flask(__name__)
app.secret_key = os.urandom(24)

# simple answer key (you can build this automatically from `questions` later)
ANSWER_KEY = {
    "q1": "Paris",
    "q2": "4"
}


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    middle_name = request.form.get('middle_name')
    email = request.form.get('email')
    fav_animal = request.form.get('fav_animal')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    user = cursor.execute(
        "SELECT * FROM USERS WHERE middle_name=? AND email=? AND fav_animal=?",
        (middle_name, email, fav_animal)
    ).fetchall()

    connection.close()

    if len(user) > 0:
        # adjust indices if your DB columns are ordered differently
        return redirect(
            url_for('home', first_name=user[0][0], last_name=user[0][1], email=user[0][2])
        )
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

    ans = cursor.execute(
        "SELECT * FROM USERS WHERE middle_name=? AND email=? AND fav_animal=?",
        (middle_name, email, fav_animal)
    ).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('login.html')
    else:
        cursor.execute(
            "INSERT INTO USERS(first_name,middle_name,last_name,email,password,fav_animal) VALUES (?,?,?,?,?,?)",
            (first_name, middle_name, last_name, email, password, fav_animal)
        )
        connection.commit()
        connection.close()
        return render_template('login.html')


@app.route('/faux')
def faux():
    return render_template('hint.html')


# show the quiz page (loads questions from question.questions)
@app.route('/quoz')
def quoz():
    return render_template('bikeQuiz.html', questions=questions)


# handle GET+POST for the quiz. function name is unique (quiz_view)
@app.route('/quiz', methods=["GET", "POST"])
def quiz_view():
    if request.method == "POST":
        
        # gather answers; if you have dynamic question ids, build this from questions
        user_answers = {
            "q1": request.form.get("q1"),
            "q2": request.form.get("q2")
        }

        feedback = {}
        results = {}
        score = 0
        total_questions = len(ANSWER_KEY)

        for q, correct in ANSWER_KEY.items():
            if user_answers.get(q) == correct:
                feedback[q] = f"{q.upper()} is correct!"
                results[q] = "correct"
                score += 1
            else:
                feedback[q] = f"{q.upper()} is incorrect."
                results[q] = "incorrect"

        if score == total_questions:
            return redirect(url_for("fish"))

        return render_template(
            "bikeQuiz.html",
            results=results,
            feedback=feedback,
            score=score,
            questions=questions
        )

    # GET request: render quiz with questions
    return render_template('bikeQuiz.html', questions=questions)


@app.route('/fish')
def fish():
    return render_template('fish1.html')

@app.route("/fischOne", methods=["POST"])
def fish_one():
    fisch_one = request.form.get('fisch_one')
    fisch_two = request.form.get('fisch_two')

    connection = sqlite3.connect('CollectedData.db')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO DATA(fisch_one, fisch_two) VALUES (?,?)",
        (fisch_one, fisch_two)
    )
    connection.commit()
    connection.close()
    return render_template('sure1.html')

@app.route('/fish1')
def fish1():
    return render_template('fish2.html')

@app.route("/fischTwo", methods=["POST"])
def fish_two():
    fisch_three = request.form.get('fisch_three')
    fisch_four = request.form.get('fisch_four')

    connection = sqlite3.connect('CollectedData.db')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO DATA(fisch_three, fisch_four) VALUES (?,?)",
        (fisch_three, fisch_four)
    )
    connection.commit()
    connection.close()
    return render_template('sure2.html')

@app.route('/fish2')
def fish2():
    return render_template('fish3.html')

@app.route("/fischThree", methods=["POST"])
def fish_three():
    fisch_five = request.form.get('fisch_five')

    connection = sqlite3.connect('CollectedData.db')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO DATA(fisch_five) VALUES (?)",
        (fisch_five)
    )
    connection.commit()
    connection.close()
    return render_template('sure3.html')

@app.route('/fish3')
def fish3():
    return render_template('final.html')


if __name__ == '__main__':
    app.run(debug=True)
