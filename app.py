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

def load_valid_words():
    valid_words = set()
    with open('static/word_list.txt', 'r') as f:
        for line in f:
            word = line.strip().lower()
            if word:  # Skip empty lines
                valid_words.add(word)
    return valid_words

def save_game_state(state):
    with open(GAME_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def clear_game_state():
    if os.path.exists(GAME_STATE_FILE):
        os.remove(GAME_STATE_FILE)

lessons = [
    {"id": 1,
     "title": "How to Play",
     "data": "Welcome to the Spelling Bee! The goal is to make words using the letters in the honeycomb. Each word must be at least 4 letters long and the center letter must be used in every word. Letters can be reused! Proper nouns and hyphenated words are not allowed.",
     "image": None},
    
    {"id": 2,
     "title": "Getting Started",
     "data": "Start by looking for common prefixes and suffixes. Words ending in -ING, -ED, -ER, -EST are often good choices.",
     "image": "lesson-2.png"},
    
    {"id": 3,
     "title": "Finding Longer Words",
     "data": "Longer words are worth more points! Look for words that combine multiple prefixes and suffixes. For example, if you see -ING and -ER, you might find words like 'running' or 'jumping'.",
     "image": "lesson-3.png"},
    
    {"id": 4,
     "title": "Common Patterns",
     "data": "Watch for common word beginnings like: NON-, UN-, CON- \n These can help you spot words quickly. Also look for compound words that combine two smaller words.",
     "image": "lesson-4.png"},
    
    {"id": 5,
     "title": "Advanced Strategies",
     "data": "Try to find words that use the same letters in different combinations. For example, if you find 'STAR', you might also find 'RATS' or 'ARTS'.",
     "image": None},
    
    {"id": 6,
     "title": "Word Families",
     "data": "Look for word families - groups of words that share the same root. For example, if you find 'PLAY', you might also find 'PLAYS', 'PLAYED', 'PLAYING', 'PLAYER'.",
     "image": None},
    
    {"id": 7,
     "title": "Time Management",
     "data": "Don't spend too long on any one word. If you're stuck, move on and come back later. Sometimes a fresh look helps spot words you missed before.",
     "image": None},
    
    {"id": 8,
     "title": "Common Mistakes",
     "data": "Watch out for proper nouns and hyphenated words - they're not allowed. Also remember that the center letter must be used in every word. Don't forget to check your spelling!",
     "image": None},
    
    {"id": 9,
     "title": "Practice Tips",
     "data": "The best way to improve is to practice regularly. Try to play at least one game each day. Keep track of the words you find to build your vocabulary.",
     "image": "lesson-9.png"},
    
    {"id": 10,
     "title": "Expert Tips",
     "data": "How could I have approached this? First: Finding the suffix -TION! Now what letters are left? (s,u,l). From this, I found SOLUTION! Think about common prefixes and suffixes: il-, un-, non-, -ist are all present.",
     "image": None},
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
    valid_words = list(load_valid_words())
    return render_template('quiz.html', game_state=game_state, valid_words=valid_words)

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