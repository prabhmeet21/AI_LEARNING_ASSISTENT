from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.pdf_reader import extract_text
from model.nlp import summarize_text, answer_question, generate_quiz


app = Flask(__name__)
CORS(app)

pdf_text_store = ""

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "✅ Backend running (HuggingFace)"

# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    global pdf_text_store

    file = request.files["file"]
    text = extract_text(file)

    pdf_text_store = text

    return jsonify({"message": "Uploaded"})

# ---------------- SUMMARY ----------------
@app.route("/summary", methods=["GET"])
def summary():
    global pdf_text_store

    if not pdf_text_store:
        return jsonify({"error": "Upload PDF first"}), 400

    result = summarize_text(pdf_text_store)

    return jsonify({"summary": result})

# ---------------- ASK ----------------
@app.route("/ask", methods=["POST"])
def ask():
    global pdf_text_store

    data = request.get_json()
    question = data.get("question", "")

    if not pdf_text_store:
        return jsonify({"error": "Upload PDF first"}), 400

    answer = answer_question(question, pdf_text_store)

    return jsonify({"answer": answer})

# ---------------- QUIZ ----------------
@app.route("/quiz", methods=["GET"])
def quiz():
    global pdf_text_store

    if not pdf_text_store:
        return jsonify({"error": "Upload PDF first"}), 400

    quiz = generate_quiz(pdf_text_store)

    return jsonify(quiz)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
