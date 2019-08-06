import os
import base64
import random
from flask import Flask, request
from model import Message 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'csrf_token' not in session:
        session['csrf_token'] = str(random.randint(10000000, 99999999))

    if request.method == 'POST':
        if request.form.get('csrf_token', None) == session['csrf_token']:
            g = Grade(
                student=request.form['student'],
                assignment=request.form['assignment'],
                grade=request.form['grade'],
            )
            g.save()

    body = """
    <html>
    <body>
    <h1>Enter Grades</h1>
    <h2>Enter a Grade</h2>
    <form method="POST">
        <label for="student">Student</label>
        <input type="text" name="student"><br>


        <label for="assignment">Assignment</label>
        <input type="text" name="assignment"><br>

        <label for="grade">Grade</label>
        <input type="text" name="grade"><br>

        <input type="hidden" name="csrf_token" value="{}">   <!-- Include the CSRF token in the form -->

        <input type="submit" value="Submit">
    </form>

    <h2>Existing Grades</h2>
    """.format(session['csrf_token'])

    for g in Grade.select():
        body += """
    <div class="grade">
    {}, {}: {}
    </div>
    """.format(g.student, g.assignment, g.grade)

    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

