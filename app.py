from flask import Flask, render_template, request, redirect, url_for
import datetime
import json
import os

app = Flask(__name__)

# Initialize logging system
LOG_FILE = 'page_visits.json'

def log_page_visit(lesson_num):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'lesson_num': lesson_num
    }
    
    # Create log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
    
    # Read existing logs
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
    
    # Add new log entry
    logs.append(log_entry)
    
    # Write back to file
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

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
    # Log the page visit
    log_page_visit(lesson_num)
    
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

@app.route('/logs')
def view_logs():
    if not os.path.exists(LOG_FILE):
        return "No logs found"
    
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
    
    return render_template('logs.html', logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5001)