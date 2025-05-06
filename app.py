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
    {"id": 1,
     "title": "Introduction to Spelling Bee",
     "data": "The New York Times Spelling Bee is a daily word game similar to the Wordle. You are provided with 7 letters: 6 normal letters, and one central core letter in yellow. Your goal is to make as many words as possible."},
    {"id": 2,
     "title": "Basic Rules",
     "data": "While making words with the given layout, you have one defining rule: The core letter must be included in every word you make. As you make more and more words, you earn points. earn enough points, and you earn the reward rank of GENIUS!"},
    {"id": 3,
     "title": "Word Length Rules",
     "data": "All of your words must be more than 4 letters, so you can't just brute force small words"},
    {"id": 4,
     "title": "Starting Strategy",
     "data": "Start small 4-5 letter words – think about the center letter, and what other letters it pairs well with"},
    {"id": 5,
     "title": "Word Endings",
     "data": "Think about common word endings to potentially more than *double* your total points! Look out for: -ed, -ing, -ion, -est -er, -ment, -able, etc."},
    {"id": 6,
     "title": "Word Beginnings",
     "data": "Don't forget common word beginnings too! This can be combined with endings for many different combinations! Look out for: non-, con-, un-, in-, or even ch-, hee- etc."},
    {"id": 7,
     "title": "Compound Words",
     "data": "Try combining words to form compound words — a sneaky way to hit all 7 letters."},
    {"id": 8,
     "title": "Persistence",
     "data": "Don't give up! Keep thinking, sound out beginnings of words, and be persistent!"},
    {"id": 9,
     "title": "Advanced Strategy",
     "data": "Look for prefixes and suffixes. When you want to reveal the pangrams, go to the next slide"},
    {"id": 10,
     "title": "Expert Tips",
     "data": "How could I have approached this? First: Finding the suffix -TION! Now what letters are left? (s,u,l). From this, I found SOLUTION! Think about common prefixes and suffixes: il-, un-, non-, -ist are all present."},
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
    current_index = ids.index(lesson_num)

    next_lesson = lessons[current_index + 1]["id"] if current_index + 1 < len(lessons) else None
    prev_lesson = lessons[current_index - 1]["id"] if current_index > 0 else None

    return render_template('learn.html', lesson_data=lesson_data, next_lesson=next_lesson, prev_lesson=prev_lesson, lessons=lessons)

@app.route('/quiz')
def quiz_home():
    game_state = get_game_state()
    return render_template('quiz.html', game_state=game_state)

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