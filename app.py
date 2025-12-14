from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from question import questions

app = Flask(__name__)
app.secret_key = os.urandom(24)

# simple answer key (you can build this automatically from `questions` later)
ANSWER_KEY = {
    "q1": "Two Wheels",
    "q2": "1847",
    "q3": "Unicode",
    "q4": "Dandy",
    "q5": "Maseru",
    "q6": "13",
    "q7": "Pigeon",
    "q8": "30",
    "q9": "Yes",
    "q10": "Innsmouth"
}


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    # Get form input
    middle_name = request.form.get('middle_name')
    email = request.form.get('email')
    fav_animal = request.form.get('fav_animal')

    # Debug (optional)
    print("Login attempt:", middle_name, email, fav_animal)

    # Connect to database
    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    # Query for user
    cursor.execute(
        """SELECT first_name, last_name, email, is_admin
           FROM USERS
           WHERE middle_name=? AND email=? AND fav_animal=?""",
        (middle_name, email, fav_animal)
    )
    user = cursor.fetchone()
    connection.close()

    # Check if a user was found
    if user:
        # Save login info in session
        session['email'] = user[2]
        session['is_admin'] = user[3]

        # Redirect based on role
        if user[3] == 1:
            return redirect(url_for('admin'))
        else:
            return redirect(
                url_for('home',
                        first_name=user[0],
                        last_name=user[1],
                        email=user[2])
            )
    else:
        # Login failed
        print("Login failed: user not found")
        return redirect('/')  # or render a "login failed" page


@app.route('/home')
def home():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')

    return render_template('userHome.html', first_name=first_name, last_name=last_name, email=email)

# Credits to one MR ZEEDERBERG for this code
@app.route("/admin")
def admin():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    connection = sqlite3.connect("CollectedData.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM DATA")
    data_rows = cursor.fetchall()
    data_columns = [description[0] for description in cursor.description]

    cursor.execute("SELECT first_name, last_name, email, is_admin FROM USERS")
    users = cursor.fetchall()

    connection.close()

    return render_template(
        "adminHome.html",
        data_rows=data_rows,
        data_columns=data_columns,
        users=users
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/make_admin/<email>")
def make_admin(email):
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    connection = sqlite3.connection("LoginData.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE USER SET is_admin = 1 WHERE email = ?", 
        (email,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("admin"))

@app.route("/admin/users")
def admin_users():
    if not session.get("is_admin"):
        return redirect(url_for('login'))
    
    connection = sqlite3.connect("LoginData.db")
    cursor = connection.cursor()

    users = cursor.execute(
        "SELECT first_name, last_name, email, is_admin FROM USERS"
    ).fetchall()

    connection.close()

    return render_template("admin_users.html", users=users)


#END credits

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
            "q2": request.form.get("q2"),
            "q3": request.form.get("q3"),
            "q4": request.form.get("q4"),
            "q5": request.form.get("q5"),
            "q6": request.form.get("q6"),
            "q7": request.form.get("q7"),
            "q8": request.form.get("q8"),
            "q9": request.form.get("q9"),
            "q10": request.form.get("q10")
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
        (fisch_five,)
    )
    connection.commit()
    connection.close()
    return render_template('sure3.html')

@app.route('/fish3')
def fish3():
    return render_template('final.html')


if __name__ == '__main__':
    app.run(debug=True)
