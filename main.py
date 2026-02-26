import random
import jsonlines
from flask import Flask, jsonify, redirect, render_template, request, session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key to the value from the .env file
app.secret_key = os.getenv('SECRET_KEY')

# Load questions for various subjects from JSONL files
questions = {
    "ce": {"en": [], "ar": []},
    "ee": {"en": [], "ar": []},
    "me": {"en": [], "ar": []},
    "coe": {"en": [], "ar": []},
    "ph": {"en": [], "ar": []},
    "ma": {"en": [], "ar": []},
    "bi": {"en": [], "ar": []},
    "ch": {"en": [], "ar": []},
}

languages = ["en", "ar"]
subjects = ["ce", "ee", "me", "coe", "ph", "ma", "bi", "ch"]

for subject in subjects:
    for lang in languages:
        filename = f'data/{subject}-{lang}.jsonl'
        with jsonlines.open(filename) as reader:
            for question in reader:
                questions[subject][lang].append(question)

@app.route('/')
def home():
    # Just renders the welcome page without any question
    return render_template('index.html')

@app.route('/ai-city')
def ai_city():
    return render_template('ai-city.html')

@app.route('/purchase-ai-city')
def purchase_ai_city():
    return render_template('purchase-ai-city.html')

@app.route('/<subject>-<lang>')
def subject_qa(subject, lang="en"):
    question_id = request.args.get('qid', type=int)  # Get question ID from query parameters
    if subject in subjects and lang in languages:
        if question_id is not None and 1 <= question_id <= len(questions[subject][lang]):
            random_question = questions[subject][lang][question_id - 1]
        else:
            random_question = random.choice(questions[subject][lang])
            question_id = questions[subject][lang].index(random_question) + 1
            return redirect(f"/{subject}-{lang}?qid={question_id}")
        return render_template(f'{subject}.html', question=random_question, question_index=question_id, lang=lang)
    else:
        return "Subject or language not found", 404

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        data = request.get_json()
        subject = data.get('subject', 'ce')
        lang = data.get('lang', 'en')
        question_id = int(data.get('question_id', 0)) - 1  # Decrease by 1 to match the list index

        if subject in subjects and lang in languages:
            question_list = questions[subject][lang]
            selected_answer = data.get('selected_answer')
            if not selected_answer or question_id >= len(question_list):
                return jsonify({"response": "Invalid question ID or answer"}), 400

            correct_answer = question_list[question_id]['answer']
            if selected_answer == correct_answer:
                response = "<span style='color: green;'>Great! Your answer is correct.</span>"
            else:
                response = f"<span style='color: red;'>Sorry! Your answer is wrong. The correct answer is: {correct_answer}</span>"

            return jsonify({'response': response})
        else:
            return jsonify({"response": "Invalid subject or language"}), 400
    except Exception as e:
        return jsonify({"response": "An error occurred processing your request"}), 500

@app.route('/clear_local_storage')
def clear_local_storage():
    return '''
    <script>
        localStorage.clear();
        alert('Local storage cleared!');
        window.location.href = '/';
    </script>
    '''

@app.route('/loaderio-54290791946ef32fa7f6691c60f6f5f6.txt')
def test():
    return app.send_static_file('loaderio-54290791946ef32fa7f6691c60f6f5f6.txt')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)