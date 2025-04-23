from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

lessons = [
    {"id":1,
     "data": " "},
    {"id":2,
     "data": " "},
    {"id":3,
     "data": " "},
    {"id":4,
     "data": " "},
    {"id":5,
     "data": " "},
    {"id":6,
     "data": " "},
    {"id":7,
     "data": " "},
    {"id":8,
     "data": " "},
    {"id":9,
     "data": " "},
    {"id":10,
     "data": " "},
    {"id":11,
     "data": " "}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    lesson_data = next((l for l in lessons if l["id"] == lesson_num), None) 

    if not lesson_data:
        return redirect(url_for('home'))

    # Find next lesson by ID
    ids = [l["id"] for l in lessons]
    try:
        current_index = ids.index(lesson_num)
        next_lesson = lessons[current_index + 1]["id"]
    except IndexError:
        next_lesson = 'quiz/1'  # No more lessons

    return render_template('learn.html', lesson_data=lesson_data, next_lesson=next_lesson, lessons=lessons)


@app.route('/quiz/<int:question_num>')
def quiz(question_num):
    return render_template('quiz.html', question_num=question_num)

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)