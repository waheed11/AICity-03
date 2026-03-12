import random
import json
import smtplib
from email.message import EmailMessage
from flask import Flask, jsonify, redirect, render_template, request, session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(basedir, '..', 'templates'), 
            static_folder=os.path.join(basedir, '..', 'static'))

@app.after_request
def add_header(response):
    # Disable caching for AR routes to ensure instant updates
    if request.path.startswith('/ar') or request.path.startswith('/get_question'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Ensure static files get updated
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Set the secret key to the value from the .env file
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-for-dev')

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
        filename = os.path.join(os.path.dirname(__file__), '..', 'data', f'{subject}-{lang}.jsonl')
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        questions[subject][lang].append(json.loads(line))
        except FileNotFoundError:
            print(f"Warning: {filename} not found.")
        except Exception as e:
            print(f"Error loading {filename}: {e}")

@app.route('/')
def home():
    # Just renders the welcome page without any question
    return render_template('index.html')

@app.route('/debug-vercel')
def debug_vercel():
    return "Vercel Sub-Route Logic is ACTIVE"

@app.route('/ai-city')
def ai_city():
    return render_template('ai-city.html')

@app.route('/purchase-ai-city')
def purchase_ai_city():
    return render_template('purchase-ai-city.html')

@app.route('/course')
def course_waitlist():
    return render_template('waitlist.html')

def send_notification(email):
    # Gmail credentials from local config, repurposed for Vercel
    msg_user = "aiabzaydi@gmail.com"
    msg_pass = "booz xjaq xzyh todh"
    
    try:
        msg = EmailMessage()
        msg.set_content(f"Success! A new user has joined the waitlist for the AI Automation Course.\n\nUser Email: {email}\n\nThe marketer agent can view the full list and reach out to them when ready.")
        msg['Subject'] = f"New AI Automation Waitlist Signup: {email}"
        msg['From'] = msg_user
        msg['To'] = "aiabzaydi@gmail.com"

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(msg_user, msg_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/api/waitlist', methods=['POST'])
def api_waitlist():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    # Append to local file (Note: On Vercel, this won't persist across redeployments)
    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'waitlist_emails.txt')
        with open(data_path, 'a') as f:
            f.write(email + '\n')
    except Exception as e:
        print(f"Error saving waitlist: {e}")
        
    # Trigger the direct email notification (Robust for Vercel)
    send_notification(email)

    return jsonify({'success': True})

# AR Experience Routes for AI City Game
@app.route('/ar')
def ar_mode():
    subject = request.args.get('subject', 'ce')
    lang = request.args.get('lang', 'ar')
    qid = request.args.get('qid', 1)
    
    # Map subject to mind file
    mind_map = {
        'ce': 'civil.mind',
        'bi': 'biology.mind',
        'ee': 'electrical.mind',
        'me': 'mechanical.mind',
        'coe': 'computer.mind',
        'ph': 'physics.mind',
        'ma': 'math.mind',
        'ch': 'chemical.mind'
    }
    target_mind = mind_map.get(subject, 'civil.mind')

    # Agent selection logic
    agents = [
        {"id": "accountant", "name_ar": "حسوبي", "role": "المحاسب", "weight": 10},
        {"id": "marketer", "name_ar": "مركوته", "role": "المسوقة", "weight": 10},
        {"id": "designer", "name_ar": "رسومه", "role": "المصممة", "weight": 10},
        {"id": "coder", "name_ar": "برموجي", "role": "المبرمج", "weight": 10},
        {"id": "writer", "name_ar": "كتوبي", "role": "الكاتب", "weight": 10},
        {"id": "planner", "name_ar": "خطوطي", "role": "المخطط", "weight": 10},
        {"id": "researcher", "name_ar": "بحوثي", "role": "الباحث", "weight": 10},
        # Fikory has lower probability (e.g., 5 weight out of 75 vs 10 for others)
        {"id": "Fikory", "name_ar": "فكوري", "role": "المنسق العام", "weight": 5}
    ]
    
    # Pick randomly but deterministically based on the question so we only need 1 audio file per question
    random.seed(f"{subject}_{lang}_{qid}")
    selected_agent = random.choices(agents, weights=[a['weight'] for a in agents], k=1)[0]
    random.seed() # Reset seed
    
    return render_template('ar-qa.html', subject=subject, lang=lang, qid=qid, agent=selected_agent, target_mind=target_mind)

@app.route('/get_question')
def get_question_api():
    subject = request.args.get('subject', 'ce')
    lang = request.args.get('lang', 'ar')
    qid_param = request.args.get('qid')
    
    if subject in questions and lang in questions[subject]:
        max_q = len(questions[subject][lang])
        if qid_param == 'random':
            actual_qid = random.randint(1, max_q)
        else:
            actual_qid = int(qid_param or 1)
            
        list_index = actual_qid - 1

        if 0 <= list_index < max_q:
            # Re-run agent generation logic deterministically based on actual_qid
            agents = [
                {"id": "accountant", "name_ar": "حسوبي", "role": "المحاسب", "weight": 10},
                {"id": "marketer", "name_ar": "مركوته", "role": "المسوقة", "weight": 10},
                {"id": "designer", "name_ar": "رسومه", "role": "المصممة", "weight": 10},
                {"id": "coder", "name_ar": "برموجي", "role": "المبرمج", "weight": 10},
                {"id": "writer", "name_ar": "كتوبي", "role": "الكاتب", "weight": 10},
                {"id": "planner", "name_ar": "خطوطي", "role": "المخطط", "weight": 10},
                {"id": "researcher", "name_ar": "بحوثي", "role": "الباحث", "weight": 10},
                {"id": "Fikory", "name_ar": "فكوري", "role": "المنسق العام", "weight": 5}
            ]
            random.seed(f"{subject}_{lang}_{actual_qid}")
            selected_agent = random.choices(agents, weights=[a['weight'] for a in agents], k=1)[0]
            random.seed() # reset

            resp_data = questions[subject][lang][list_index].copy()
            resp_data['agent'] = selected_agent
            resp_data['qid'] = actual_qid
            return jsonify(resp_data)
            
    return jsonify({"error": "Question not found"}), 404

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