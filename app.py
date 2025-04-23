from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime
import json
import os

app = Flask(__name__)

# Initialize logging system
LOG_FILE = 'page_visits.json'
SPELLING_BEE_RESULTS_FILE = 'spelling_bee_results.json'
GAME_STATE_FILE = 'game_state.json'

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

def save_spelling_bee_results(game_data):
    # Create results file if it doesn't exist
    if not os.path.exists(SPELLING_BEE_RESULTS_FILE):
        with open(SPELLING_BEE_RESULTS_FILE, 'w') as f:
            json.dump([], f)
    
    # Read existing results
    with open(SPELLING_BEE_RESULTS_FILE, 'r') as f:
        results = json.load(f)
    
    # Add new result
    results.append(game_data)
    
    # Write back to file
    with open(SPELLING_BEE_RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

def get_game_state():
    if not os.path.exists(GAME_STATE_FILE):
        return {
            'start_time': None,
            'found_words': [],
            'score': 0
        }
    
    with open(GAME_STATE_FILE, 'r') as f:
        return json.load(f)

def save_game_state(state):
    with open(GAME_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def clear_game_state():
    if os.path.exists(GAME_STATE_FILE):
        os.remove(GAME_STATE_FILE)

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

@app.route('/quiz')
def quiz_home():
    game_state = get_game_state()
    return render_template('quiz.html', game_state=game_state)

@app.route('/quiz/<int:question_num>')
def quiz(question_num):
    return redirect(url_for('quiz_home'))

@app.route('/update_game_state', methods=['POST'])
def update_game_state():
    game_data = request.get_json()
    current_state = get_game_state()
    
    # If this is a new game, set the start time
    if not current_state['start_time']:
        current_state['start_time'] = datetime.datetime.now().isoformat()
    
    # Update the game state
    current_state['found_words'] = game_data['foundWords']
    current_state['score'] = game_data['score']
    save_game_state(current_state)
    
    return jsonify({"status": "success"})

@app.route('/end_game', methods=['POST'])
def end_game():
    game_data = request.get_json()
    save_spelling_bee_results(game_data)
    clear_game_state()
    return jsonify({"status": "success"})

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

@app.route('/end-quiz')
def end_quiz():
    game_state = get_game_state()
    return render_template('quiz.html', game_state=game_state, game_ended=True)

if __name__ == "__main__":
    app.run(debug=True, port=5001)