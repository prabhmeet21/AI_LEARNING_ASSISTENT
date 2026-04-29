import streamlit as st
import requests

st.title("📚 AI Learning Assistant")

# ---------------- UPLOAD ----------------
file = st.file_uploader("Upload PDF", type="pdf")

if file:
    files = {"file": file}
    res = requests.post("http://127.0.0.1:5000/upload", files=files)

    if res.status_code == 200:
        st.success("✅ PDF Uploaded Successfully")
    else:
        st.error(res.json().get("error", "Upload failed"))

# ---------------- SUMMARY ----------------
st.subheader("📄 Summary")

if st.button("Generate Summary"):
    res = requests.get("http://127.0.0.1:5000/summary")

    if res.status_code == 200:
        st.write(res.json().get("summary"))
    else:
        st.error(res.json().get("error"))

# ---------------- ASK ----------------
st.subheader("❓ Ask Question")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question")
    else:
        res = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"question": question}
        )

        if res.status_code == 200:
            st.write(res.json().get("answer"))
        else:
            st.error(res.json().get("error"))



# ---------------- QUIZ ----------------
if st.button("🧠 Generate Quiz"):
    res = requests.get("http://127.0.0.1:5000/quiz")

    if res.status_code == 200:
        st.session_state.quiz = res.json()
        st.session_state.submitted = False
        st.session_state.answers = {}

# Show quiz
if "quiz" in st.session_state:
    quiz = st.session_state.quiz

    for i, q in enumerate(quiz):
        st.subheader(f"Q{i+1}: {q['question']}")

        st.session_state.answers[i] = st.radio(
            "Choose one:",
            q["options"],
            key=f"q{i}",
            disabled=st.session_state.get("submitted", False)  # 🔥 lock after submit only
        )

    # Submit button
    if not st.session_state.get("submitted", False):
        if st.button("✅ Submit Answers"):
            st.session_state.submitted = True

    # Show result AFTER submit
    if st.session_state.get("submitted", False):
        score = 0

        for i, q in enumerate(quiz):
            user_ans = st.session_state.answers[i]

            if user_ans == q["answer"]:
                st.success(f"Q{i+1}: Correct ✅")
                score += 1
            else:
                st.error(f"Q{i+1}: Wrong ❌ | Correct: {q['answer']}")

        st.success(f"🎯 Final Score: {score} / {len(quiz)}")
   
