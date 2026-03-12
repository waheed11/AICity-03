import json
import os
import random
import time
import requests

# Ensure the output directory exists
out_dir = "../static/audio"
os.makedirs(out_dir, exist_ok=True)

# API Configuration
ELEVENLABS_API_KEY = "sk_9edec1a7745cc45a1a1066b89359829abfe76e89e3084408"
TTS_MODEL = "eleven_turbo_v2_5"

AGENT_VOICES = {
    "accountant": "VR6AewLTigWG4xSOukaG",
    "designer": "VwC51uc4PUblWEJSPzeo",
    "marketer": "EXAVITQu4vr4xnSDxMaL",
    "coder": "onwK4e9ZLuTAKqWW03F9",
    "researcher": "N2lVS1w4EtoT3dr4eOWO",
    "writer": "VR6AewLTigWG4xSOukaG", # Fallback for deleted D38..
    "planner": "TX3LPaxmHKxFdv7VOQHJ",
    "Fikory": "yXEnnEln9armDCyhkXcA"  # Using Thinkorry / operationer
}

AGENTS_CONFIG = [
    {"id": "accountant", "name_ar": "حسوبي", "role": "المحاسب", "weight": 10},
    {"id": "marketer", "name_ar": "مركوته", "role": "المسوقة", "weight": 10},
    {"id": "designer", "name_ar": "رسومه", "role": "المصممة", "weight": 10},
    {"id": "coder", "name_ar": "برموجي", "role": "المبرمج", "weight": 10},
    {"id": "writer", "name_ar": "كتوبي", "role": "الكاتب", "weight": 10},
    {"id": "planner", "name_ar": "خطوطي", "role": "المخطط", "weight": 10},
    {"id": "researcher", "name_ar": "بحوثي", "role": "الباحث", "weight": 10},
    {"id": "Fikory", "name_ar": "فكوري", "role": "المنسق العام", "weight": 5}
]

def generate_tts(text, voice_id, filepath):
    if os.path.exists(filepath):
        print(f"Skipping {filepath}, already exists.")
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    data = {
        "text": text,
        "model_id": TTS_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print(f"Generating audio for {filepath} ({len(text)} chars)...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print("Success!")
    else:
        print(f"Error {response.status_code}: {response.text}")

subjects_to_test = {
    "ce": {"profession_ar": "بش مهندس مدني"},
    "bi": {"profession_ar": "عالم الاحياء"},
    "ee": {"profession_ar": "بش مهندس كهرباء"},
    "me": {"profession_ar": "بش مهندس ميكانيكا"},
    "coe": {"profession_ar": "بش مهندس حاسب"},
    "ph": {"profession_ar": "عالم الفيزياء"},
    "ma": {"profession_ar": "عالم الرياضيات"},
    "ch": {"profession_ar": "عالم الكيمياء"}
}
lang = "ar"

# 1. Generate Global Fikory Audio (one file per subject)
for subject, info in subjects_to_test.items():
    fikory_text = f"انا فكوري المنسق العام لوكالات الذكاء الاصطناعي اود اخبارك يا {info['profession_ar']} ان تدريبك للانظمة يسير بشكل ممتاز وعليه قررت المدينة اعطاءك 2 عملة رقمية"
    filepath = os.path.join(out_dir, f"{subject}_{lang}_Fikory.mp3")
    generate_tts(fikory_text, AGENT_VOICES["Fikory"], filepath)

# 2. Iterate Questions Data
for subject, info in subjects_to_test.items():
    data_path = f"../data/{subject}-{lang}.jsonl"
    if not os.path.exists(data_path):
        continue
        
    with open(data_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        try:
            q = json.loads(line)
        except Exception:
            continue
            
        qid = i + 1
        
        # Exact identical seed logic from main.py to sync agents
        random.seed(f"{subject}_{lang}_{qid}")
        selected_agent = random.choices(AGENTS_CONFIG, weights=[a['weight'] for a in AGENTS_CONFIG], k=1)[0]
        random.seed()
        
        # Skip Fikory because we already generated the static Fikory file, and Fikory doesn't ask questions
        if selected_agent["id"] == "Fikory":
            continue
            
        agent_depts = {
            'accountant': 'المحاسبة', 'marketer': 'التسويق', 'designer': 'التصميم',
            'coder': 'البرمجة', 'writer': 'الكتابة', 'planner': 'التخطيط', 'researcher': 'البحث'
        }
        dept = agent_depts.get(selected_agent["id"], selected_agent["role"])
        is_female = selected_agent["name_ar"].endswith('ة') or selected_agent["name_ar"].endswith('ه')
        agent_title = 'وكيلة' if is_female else 'وكيل'

        narrative = f"أهلاً يا {info['profession_ar']}، أنا {agent_title} {dept} في المدينة وأرجو منك مساعدتي في الإجابة على السؤال التالي..."
        
        q_text = q.get("question", "")
        options_text = ""
        for opt in ["A", "B", "C", "D"]:
            if opt in q:
                options_text += f", الخيار {opt}: {q[opt]}"
                
        full_text = f"{narrative} {q_text} {options_text}"
        
        filepath = os.path.join(out_dir, f"{subject}_{lang}_{qid}_{selected_agent['id']}.mp3")
        generate_tts(full_text, AGENT_VOICES[selected_agent["id"]], filepath)
        
        # Sleep slightly to respect api limits on high volume
        time.sleep(0.5)

print("Batch processing complete.")
