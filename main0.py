from flask import Flask, render_template, request, jsonify
import random
import jsonlines

app = Flask(__name__)

  # Load questions for various subjects from JSONL files
ce_ar_questions = []
ee_ar_questions = []
me_ar_questions = []
coe_ar_questions = []
ph_ar_questions = []
ma_ar_questions = []
bi_ar_questions = []
ch_ar_questions = []

with jsonlines.open('data/ce-ar.jsonl') as reader:
      for question in reader:
          ce_ar_questions.append(question)
with jsonlines.open('data/ee-ar.jsonl') as reader:
      for question in reader:
          ee_ar_questions.append(question)
with jsonlines.open('data/me-ar.jsonl') as reader:
      for question in reader:
          me_ar_questions.append(question)
with jsonlines.open('data/coe-ar.jsonl') as reader:
      for question in reader:
          coe_ar_questions.append(question)
with jsonlines.open('data/ph-ar.jsonl') as reader:
      for question in reader:
          ph_ar_questions.append(question)
with jsonlines.open('data/ma-ar.jsonl') as reader:
      for question in reader:
          ma_ar_questions.append(question)
with jsonlines.open('data/bi-ar.jsonl') as reader:
      for question in reader:
          bi_ar_questions.append(question)
with jsonlines.open('data/ch-ar.jsonl') as reader:
      for question in reader:
          ch_ar_questions.append(question)

@app.route('/')
def home():
      # Just renders the welcome page without any question
      return render_template('index.html')

@app.route('/<subject>-ar')
def subject_qa(subject):
      # Dynamic route to handle different subjects
      subjects = {
          "ce": ce_ar_questions,
          "ee": ee_ar_questions,
          "me": me_ar_questions,
          "coe": coe_ar_questions,
          "ph": ph_ar_questions,
          "ma": ma_ar_questions,
          "bi": bi_ar_questions,
          "ch": ch_ar_questions,
      }
      if subject in subjects:
          random_question = random.choice(subjects[subject])
          question_index = subjects[subject].index(random_question)
          return render_template(f'{subject}-ar.html', question=random_question, question_index=question_index)
      else:
          return "Subject not found", 404

@app.route('/check_answer', methods=['POST'])
def check_answer():
      data = request.get_json()
      subject = data.get('subject', 'ce')  # Default to 'ce' if not specified
      question_id = int(data['question_id'])

      subjects = {
          "ce": ce_ar_questions,
          "ee": ee_ar_questions,
          "me": me_ar_questions,
          "coe": coe_ar_questions,
          "ph": ph_ar_questions,
          "ma": ma_ar_questions,
          "bi": bi_ar_questions,
          "ch": ch_ar_questions,
      }

      if subject in subjects:
          question_list = subjects[subject]
          selected_answer = data['selected_answer']
          correct_answer = question_list[question_id]['answer']

          if selected_answer == correct_answer:
              response = "<span style='color: green;'>Great! Your answer is correct.</span>"
          else:
              response = f"<span style='color: red;'>Sorry! Your answer is wrong. The correct answer is: {correct_answer} </span>"

          return jsonify({'response': response})
      else:
          return jsonify({"response": "Invalid subject"}), 400

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)