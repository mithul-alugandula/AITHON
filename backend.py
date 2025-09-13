from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# In-memory store (demo only)
user_progress = {
    "subject": "Physics",
    "streak": 5,
    "mastery": 68,
    "hours": 8.5,
    "topics_completed": 4,
    "topics_total": 12
}

@app.route("/api/progress", methods=["GET"])
def get_progress():
    return jsonify(user_progress)

@app.route("/api/progress", methods=["POST"])
def update_progress():
    data = request.json
    for k, v in data.items():
        user_progress[k] = v
    return jsonify({"status": "updated", "progress": user_progress})

@app.route("/api/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"summary": "No text provided."})
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
    summary = '. '.join(sentences[:3])
    if len(sentences) > 3:
        summary += "..."
    return jsonify({"summary": summary})

@app.route("/api/quiz", methods=["POST"])
def quiz():
    text = request.json.get("text", "")
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
    questions = []
    for i in range(min(5, len(sentences))):
        words = sentences[i].split()
        if len(words) < 6:
            continue
        idx = len(words) // 2
        answer = words[idx]
        words[idx] = "_____"
        question = ' '.join(words)
        questions.append({"q": question, "answer": answer})
    return jsonify({"quiz": questions})

@app.route("/api/recommend", methods=["POST"])
def recommend():
    profile = request.json or {}
    subject = profile.get("subject", "General Studies")
    plans = [
        f"45 min focused practice on {subject} + 15 min conceptual reading",
        f"30 min problem solving + 20 min review notes + 10 min flashcards",
        f"1 hr mix of theory & practice on {subject}"
    ]
    resources = {
        "Physics": ["H.C. Verma - Concepts of Physics", "Khan Academy Physics", "Walter Lewin MIT Lectures"],
        "Mathematics": ["Art of Problem Solving", "3Blue1Brown videos", "Khan Academy Math"],
        "Chemistry": ["NCERT Chemistry", "CrashCourse Chemistry", "Organic Chemistry Tutor"],
        "Biology": ["Campbell Biology", "Bozeman Science", "Khan Academy Biology"]
    }
    return jsonify({
        "plan": random.choice(plans),
        "resources": resources.get(subject, ["General study tips", "Khan Academy"])
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
