from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import jsonlines

app = Flask(__name__)

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

# Dynamically load questions based on language and subject
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

@app.route('/<subject>-<lang>')
def subject_qa(subject, lang="en"):
    question_id = request.args.get('qid', type=int)  # Get question ID from query parameters
    if subject in subjects and lang in languages:
        if question_id is not None and question_id < len(questions[subject][lang]):
            random_question = questions[subject][lang][question_id]
        else:
            random_question = random.choice(questions[subject][lang])
            question_id = questions[subject][lang].index(random_question)
        return render_template(f'{subject}.html', question=random_question, question_index=question_id, lang=lang)
    else:
        return "Subject or language not found", 404

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        # Decode JSON data sent with POST request
        data = request.get_json()
        subject = data.get('subject')
        lang = data.get('lang', 'en')  # Default language
        question_id = data.get('question_id')
        selected_answer = data.get('selected_answer')
        # Print the received values for debugging
        print(f"Subject: {subject}, Language: {lang}, Question ID: {question_id}, Selected Answer: {selected_answer}")

        # Validate input
        if subject not in questions or lang not in questions[subject]:
            return jsonify({"response": "Invalid subject or language"}), 400

        # Find the question using the provided ID
        question_list = questions[subject][lang]
        matched_question = next((item for item in question_list if item['id'] == question_id), None)

        # Print the matched question for debugging
        print(f"Matched Question: {matched_question}")

        if not matched_question:
            return jsonify({"response": "Question not found"}), 404

        # Check if selected answer is correct
        if selected_answer == correct_answer:
              response = "<span style='color: green;'>Great! Your answer is correct.</span>"
        else:
              response = f"<span style='color: red;'>Sorry! Your answer is wrong. The correct answer is: {correct_answer} </span>"

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)