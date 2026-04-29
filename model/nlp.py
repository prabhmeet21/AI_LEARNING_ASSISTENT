from transformers import pipeline

# Small model (lightweight)
generator = pipeline(
    "text-generation",
    model="sshleifer/tiny-gpt2"
)

# ---------------- SUMMARY ----------------
def summarize_text(text):
    text = text[:1000]

    prompt = f"Summarize this text:\n{text}"

    result = generator(prompt, max_length=120)

    return result[0]["generated_text"]


# ---------------- QUESTION ANSWER ----------------
def answer_question(question, context):
    context = context[:1000]

    prompt = f"{context}\n\nQuestion: {question}\nAnswer:"

    result = generator(prompt, max_length=120)

    return result[0]["generated_text"]


# ---------------- QUIZ (FIXED) ----------------
def generate_quiz(text):
    text = text[:1000]

    # Take meaningful sentences
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 30][:10]

    quiz = []

    for s in sentences:
        question = f"What is the meaning of: '{s}'?"

        options = [
            s[:50],  # correct answer
            "This statement is incorrect",
            "None of the above"
        ]

        quiz.append({
            "question": question,
            "options": options,
            "answer": options[0]
        })

    return quiz




    
