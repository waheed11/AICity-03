import json
import os
import random
import time
from openai import OpenAI

# Initialize OpenAI Client (Make sure OPENAI_API_KEY is in environment)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Ensure the output directory exists
out_dir = "../static/audio"
os.makedirs(out_dir, exist_ok=True)

# OpenAI Voice Mapping
# Available voices: alloy, echo, fable, onyx, nova, shimmer
AGENT_VOICES = {
    "marketer": "nova",       # Female
    "designer": "shimmer",    # Female
    "accountant": "echo",     # Male
    "coder": "onyx",          # Male
    "researcher": "fable",    # Male
    "writer": "alloy",        # Neutral/Male
    "planner": "echo",        # Male (Reused)
    "Fikory": "fable"         # Male (Reused)
}

AGENTS_CONFIG = [
    {"id": "accountant", "name_ar": "حسوبي", "role": "المحاسب", "weight": 10},
    {"id": "marketer", "name_ar": "مركوته", "role": "المسوقة", "weight": 10},
    {"id": "designer", "name_ar": "رسومه", "role": "المصممة", "weight": 10},
    {"id": "coder", "name_ar": "برموجي", "role": "المبرمج", "weight": 10},
    {"id": "writer", "name_ar": "كتوبي", "role": "كاتب المحتوى", "weight": 10},
    {"id": "planner", "name_ar": "خطوطي", "role": "المخطط", "weight": 10},
    {"id": "researcher", "name_ar": "بحوثي", "role": "الباحث", "weight": 10},
    {"id": "Fikory", "name_ar": "فكوري", "role": "المنسق العام", "weight": 5}
]

def generate_tts(text, voice_id, filepath):
    if os.path.exists(filepath):
        print(f"Skipping {filepath}, already exists.")
        return

    print(f"Generating audio for {filepath} ({len(text)} chars) with voice '{voice_id}'...")
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_id,
            input=text
        )
        response.stream_to_file(filepath)
        print("Success!")
    except Exception as e:
        print(f"Error generating {filepath}: {e}")

subjects_to_test = {
    "ce": {"profession_ar": "بش مهندس مدني", "profession_en": "Civil Engineering"},
    "bi": {"profession_ar": "عالم الاحياء", "profession_en": "Biology"},
    "ee": {"profession_ar": "بش مهندس كهرباء", "profession_en": "Electrical Engineering"},
    "me": {"profession_ar": "بش مهندس ميكانيكا", "profession_en": "Mechanical Engineering"},
    "coe": {"profession_ar": "بش مهندس حاسب", "profession_en": "Computer Engineering"},
    "ph": {"profession_ar": "عالم الفيزياء", "profession_en": "Physics"},
    "ma": {"profession_ar": "عالم الرياضيات", "profession_en": "Mathematics"},
    "ch": {"profession_ar": "عالم الكيمياء", "profession_en": "Chemistry"}
}

# English translations for direct roles
role_en_map = {
    "المحاسب": "Accountant", "المسوقة": "Marketer", "المصممة": "Designer",
    "المبرمج": "Programmer", "كاتب المحتوى": "Content Writer", "المخطط": "Planner",
    "الباحث": "Researcher"
}

# The user can run this script for either "ar" or "en"
for LANG_TO_GENERATE in ["ar", "en"]:
    print(f"\n--- Generating for language: {LANG_TO_GENERATE} ---")
    # 1. Generate Global Fikory Audio
    for subject, info in subjects_to_test.items():
        if LANG_TO_GENERATE == 'ar':
            fikory_text = f"انا فكوري المنسق العام للمدينة، اود اخبارك يا {info['profession_ar']} ان تدريبك للانظمة يسير بشكل ممتاز وعليه قررت المدينة اعطاءك 2 عملة رقمية"
        else:
            fikory_text = f"Welcome {info['profession_en']} expert, I am Fikory the general coordinator of the city. Thank you for your efforts, you have earned two coins."
            
        filepath = os.path.join(out_dir, f"{subject}_{LANG_TO_GENERATE}_Fikory.mp3")
        generate_tts(fikory_text, AGENT_VOICES["Fikory"], filepath)

    # 2. Iterate Questions Data
    for subject, info in subjects_to_test.items():
        data_path = f"../data/{subject}-{LANG_TO_GENERATE}.jsonl"
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
            
            # Exact identical seed logic to sync agents between frontend and audio gen
            random.seed(f"{subject}_{LANG_TO_GENERATE}_{qid}")
            selected_agent = random.choices(AGENTS_CONFIG, weights=[a['weight'] for a in AGENTS_CONFIG], k=1)[0]
            random.seed()
            
            # Skip Fikory (handled above)
            if selected_agent["id"] == "Fikory":
                continue
                
            is_female = selected_agent["name_ar"] in ['مركوته', 'رسومه']
            
            if LANG_TO_GENERATE == 'ar':
                role_ar = selected_agent["role"]
                narrative = f"أهلاً يا {info['profession_ar']}، أنا {role_ar} في المدينة وأرجو منك مساعدتي في الإجابة على السؤال التالي."
            else:
                role_en = role_en_map.get(selected_agent["role"], selected_agent["role"])
                narrative = f"Hello {info['profession_en']} expert, I am the {role_en} in the city, and I need your help with this question."

            q_text = q.get("question", "")
            
            # We REMOVED reading out options A, B, C, D to save cost and make gameplay faster!
            full_text = f"{narrative} {q_text}"
            
            filepath = os.path.join(out_dir, f"{subject}_{LANG_TO_GENERATE}_{qid}_{selected_agent['id']}.mp3")
            generate_tts(full_text, AGENT_VOICES[selected_agent["id"]], filepath)
            
            # Sleep slightly to respect api limits on high volume (OpenAI limit is generous but good practice)
            time.sleep(0.1)

print("Batch processing complete.")
