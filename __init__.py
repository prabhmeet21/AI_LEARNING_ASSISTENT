from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="sshleifer/tiny-gpt2"
)

def summarize_text(text):
    text = text[:1000]
    prompt = f"Summarize:\n{text}"
    result = generator(prompt, max_length=100)
    return result[0]["generated_text"]


def answer_question(question, context):
    context = context[:1000]
    prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
    result = generator(prompt, max_length=100)
    return result[0]["generated_text"]


def generate_quiz(text):
    text = text[:1000]

    prompt = f"""
Create 5 multiple choice questions from this text.
Each question must have:
- 1 correct answer
- 2 wrong answers

Format:
Q1:
A)
B)
C)
Correct Answer:

Text:
{text}
"""

    result = generator(prompt, max_length=300)
    return result[0]["generated_text"]