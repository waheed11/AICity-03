# AI City - Digital Companion App

> Developer documentation for the AI City board game's web-based question engine.

**Live**: [https://ai-fun-learning.com](https://ai-fun-learning.com)  
**Buy the Game**: [Salla Store](https://salla.sa/ai-fun-learning)  
**Repository**: [github.com/waheed11/AICity-03](https://github.com/waheed11/AICity-03)

---

## Overview

AI City is an innovative board game that simulates scientists and engineers training AI systems for their city. Players answer subject-specific questions via this digital companion app by scanning QR codes on their specialization cards. The most accurate team earns control of the City Research Center.

This application serves as the **question engine**: it delivers randomized questions, validates answers, provides audio feedback, and tracks session progress.

---

## Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Backend         | Flask (Python 3.12)                 |
| Data Format     | JSONLines (`.jsonl`)                |
| Data Library    | `jsonlines` 4.x                     |
| Environment     | `python-dotenv`                     |
| Deployment      | Vercel (Python Serverless Runtime)  |
| Dependency Mgmt | Poetry                              |

---

## API Endpoints

### `GET /<subject>-<lang>`

Renders the quiz UI for a given subject and language.

- **Path Parameters**:
  - `subject`: One of `ce`, `ee`, `me`, `coe`, `ph`, `ma`, `bi`, `ch`
  - `lang`: `en` or `ar`
- **Query Parameters**:
  - `qid` (optional, int): Load a specific question by ID. If omitted, a random question is selected and the client is redirected to a `?qid=` URL.

**Example**: `GET /bi-en?qid=3` — loads the 3rd Biology question in English.

### `POST /check_answer`

Validates the player's submitted answer.

**Request Body** (JSON):
```json
{
  "subject": "bi",
  "lang": "en",
  "question_id": 3,
  "selected_answer": "B"
}
```

**Response** (JSON):
```json
{
  "response": "<span style='color: green;'>Great! Your answer is correct.</span>"
}
```

Audio is triggered client-side based on whether the response contains `green` (correct) or not (incorrect).

### `GET /clear_local_storage`

Utility endpoint that clears the browser's `localStorage` and redirects to `/`.

### Other Pages

| Route               | Description                  |
|----------------------|------------------------------|
| `GET /`              | Landing page (AR/EN toggle)  |
| `GET /ai-city`       | Product info page            |
| `GET /purchase-ai-city` | Purchase links             |
| `GET /about`         | About the company            |
| `GET /contact`       | Contact page                 |

---

## Data Format

Questions are stored as **JSONLines** files in the `data/` directory.

### File Naming

```
data/<subject>-<lang>.jsonl
```

**Subjects**: `bi` (Biology), `ce` (Civil Engineering), `ch` (Chemistry), `coe` (Computer Engineering), `ee` (Electrical Engineering), `ma` (Mathematics), `me` (Mechanical Engineering), `ph` (Physics)

### Record Schema

Each line is a single JSON object:

```json
{"question": "What is the powerhouse of the cell?", "A": "Golgi apparatus", "B": "Mitochondria", "C": "Ribosome", "D": "Endoplasmic reticulum", "answer": "B"}
```

| Field      | Type   | Description                     |
|------------|--------|---------------------------------|
| `question` | string | The question text               |
| `A`        | string | Option A                        |
| `B`        | string | Option B                        |
| `C`        | string | Option C                        |
| `D`        | string | Option D                        |
| `answer`   | string | Correct option key (A/B/C/D)    |

---

## Frontend Logic

### Session Tracking

The client uses `localStorage` to track a `globalQuestionCount`. After **16 questions**, `localStorage` is cleared automatically — matching the board game's win condition of filling 16 coin slots.

### Audio Feedback

Located in `static/audio/`:
- `correct_answer.wav` — played on correct answer
- `wrong_answer.wav` — played on incorrect answer

### Language Switching

The `switchLanguage.js` script toggles between `/subject-en` and `/subject-ar` while preserving the current `qid`.

---

## Project Structure

```
AICity-03/
├── api/
│   └── index.py              # Flask app (Vercel entry point)
├── data/
│   ├── bi-en.jsonl            # Biology questions (English)
│   ├── bi-ar.jsonl            # Biology questions (Arabic)
│   ├── ce-en.jsonl, ce-ar.jsonl, ...
│   └── ...                    # 8 subjects x 2 languages = 16 files
├── static/
│   ├── audio/                 # correct_answer.wav, wrong_answer.wav
│   ├── css/                   # Stylesheets
│   ├── image/                 # Logos and product images
│   └── scripts/               # switchLanguage.js
├── templates/
│   ├── base.html              # Base layout
│   ├── index.html             # Landing page
│   ├── ai-city.html           # Product page
│   ├── bi.html, ce.html, ...  # Per-subject quiz templates
│   └── ...
├── util-steps/                # Question management scripts
│   ├── insert-questions.py    # Bulk insert with similarity checks
│   ├── keep-keys.py
│   └── unique.py
├── utilities/                 # Data conversion and cleanup tools
├── main.py                    # Local dev entry point
├── requirements.txt           # Vercel dependencies
├── .env                       # SECRET_KEY config
└── Game Instructions-ar-en.pdf
```

---

## Development Setup

### Prerequisites
- Python 3.12+
- [Poetry](https://python-poetry.org/)

### Install & Run

```bash
# Install dependencies
poetry install

# Configure environment
echo "SECRET_KEY=your-secret-key" > .env

# Start local server
poetry run python main.py
# Server runs on http://localhost:5000
```

### Adding Questions

Use `util-steps/insert-questions.py` to add new questions to a `.jsonl` file. The script includes **Levenshtein distance checks** to prevent duplicate/similar questions from being inserted.

---

## Deployment

The application is deployed on **Vercel** using the Python serverless runtime.

- **Entry point**: `api/index.py`
- **Dependencies**: Declared in `requirements.txt`
- **Environment variable**: Set `SECRET_KEY` in the Vercel dashboard

---

## Game Context

> For full gameplay instructions, see [Game Instructions-ar-en.pdf](Game%20Instructions-ar-en.pdf).

AI City is a competitive board game for 2-4 players. Teams work in city locations (Studio, Library, Workshop, Laboratory), scanning QR codes to answer questions in their specialization. Correct answers earn digital coins. The first team to fill 16 coin slots wins control of the City Research Center.
