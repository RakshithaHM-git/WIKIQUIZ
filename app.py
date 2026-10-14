
import csv
import json
import random
import re
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "wikipedia_dataset.csv"
HISTORY_FILE = BASE_DIR / "data" / "quiz_history.json"
QUIZ_SIZE = 5

st.set_page_config(
    page_title="WikiQuiz",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7ff, #eef5ff);
}
.main-title {
    text-align: center;
    color: #263b80;
    font-size: 46px;
    font-weight: 800;
}
.subtitle {
    text-align: center;
    color: #52617d;
    font-size: 18px;
    margin-bottom: 28px;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


def clean(value):
    value = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", value).strip()


@st.cache_data
def load_articles():
    if not DATA_FILE.exists():
        return []

    articles = []
    with open(DATA_FILE, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            name = clean(row.get("name"))
            description = clean(row.get("description"))
            abstract = clean(row.get("abstract"))
            content = description if len(description) >= 80 else abstract

            if name and content:
                articles.append({
                    "name": name,
                    "description": description or abstract,
                    "content": content,
                    "url": clean(row.get("url"))
                })
    return articles


def load_history():
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save_history(history):
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(
            json.dumps(history, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except OSError:
        st.warning("Quiz completed, but history could not be saved.")


def make_questions(article, articles):
    sentences = re.split(r"(?<=[.!?])\s+", article["content"])
    sentences = [s.strip() for s in sentences if len(s.strip()) >= 30]
    distractors = [
        a["name"] for a in articles
        if a["name"] != article["name"]
    ]
    random.shuffle(distractors)

    questions = [{
        "question": "What is this article mainly about?",
        "options": [],
        "answer": article["name"]
    }]
    names = [article["name"]] + distractors[:3]
    random.shuffle(names)
    questions[0]["options"] = names

    if sentences:
        options = [article["name"]] + distractors[:3]
        random.shuffle(options)
        questions.append({
            "question": "Which Wikipedia article matches this information?\n\n"
                        + sentences[0][:350],
            "options": options,
            "answer": article["name"]
        })

    if len(sentences) >= 2:
        questions.append({
            "question": "According to this article, is the following statement true?\n\n"
                        + sentences[1][:350],
            "options": ["True", "False", "Cannot be determined", "None of the above"],
            "answer": "True"
        })

    if len(sentences) >= 3:
        sentence = sentences[2][:350]
        questions.append({
            "question": "Which statement is supported by the article?",
            "options": [sentence, "The article describes a programming language.",
                        "The article explains a mathematical formula.",
                        "The article is about computer hardware."],
            "answer": sentence
        })

    if distractors:
        options = [article["name"]] + distractors[:3]
        random.shuffle(options)
        questions.append({
            "question": "Which topic is most directly connected to this article?",
            "options": options,
            "answer": article["name"]
        })

    random.shuffle(questions)
    return questions[:QUIZ_SIZE]


articles = load_articles()

st.markdown('<div class="main-title">🧠 WikiQuiz</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Explore Wikipedia • Test Your Knowledge • Track Your Progress</div>',
    unsafe_allow_html=True
)

if not articles:
    st.error("Dataset not found. Check that data/wikipedia_dataset.csv exists.")
    st.stop()

history = load_history()

with st.sidebar:
    st.title("🧭 Navigation")
    page = st.radio(
        "Choose a page",
        ["🏠 Home", "🔍 Start Quiz", "📚 Quiz History", "📊 Performance"]
    )
    st.divider()
    st.caption(f"📖 {len(articles):,} articles available")


if page == "🏠 Home":
    st.subheader("Welcome to WikiQuiz!")
    st.write("Discover interesting topics and challenge yourself with questions "
             "based on your Wikipedia dataset.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Articles Available", f"{len(articles):,}")
    c2.metric("Quizzes Completed", len(history))
    total_q = sum(int(h.get("total_questions", h.get("total", 0))) for h in history)
    c3.metric("Questions Answered", total_q)

    st.info("Use the sidebar to search for a topic and start your quiz.")
    st.markdown("### ✨ Features")
    st.markdown("""
    - 🔎 Search Wikipedia topics
    - 📝 Multiple-choice quiz questions
    - 🎯 Instant scoring and results
    - 📚 Quiz history
    - 📊 Performance statistics
    """)

elif page == "🔍 Start Quiz":
    st.subheader("🔎 Find a Wikipedia Topic")
    search = st.text_input("Enter a topic keyword", placeholder="e.g. Science, Python, India")

    matches = [
        a for a in articles
        if search.lower() in a["name"].lower()
    ] if search else articles

    if not matches:
        st.warning("No matching topics found. Try another keyword.")
    else:
        options = matches[:100]
        selected_name = st.selectbox(
            "Choose an article",
            [a["name"] for a in options]
        )
        article = next(a for a in options if a["name"] == selected_name)

        with st.expander("📖 Read article details"):
            st.write(article["description"] or "No description available.")
            if article["url"]:
                st.markdown(f"[Read Wikipedia source]({article['url']})")

        if st.button("🚀 Generate Quiz", type="primary"):
            questions = make_questions(article, articles)
            if len(questions) < QUIZ_SIZE:
                st.warning("Not enough questions could be generated for this topic. Try another article.")
            else:
                st.session_state.quiz_article = article
                st.session_state.quiz_questions = questions
                st.session_state.quiz_submitted = False
                st.session_state.quiz_key = random.randint(1, 999999)

        if "quiz_questions" in st.session_state and not st.session_state.get("quiz_submitted", False):
            quiz_article = st.session_state.quiz_article
            questions = st.session_state.quiz_questions
            st.divider()
            st.markdown(f"### 📝 Quiz: {quiz_article['name']}")
            answers = []

            with st.form(f"quiz_form_{st.session_state.quiz_key}"):
                for i, q in enumerate(questions):
                    st.markdown(f"**Question {i + 1} of {len(questions)}**")
                    st.write(q["question"])
                    answers.append(
                        st.radio(
                            "Choose your answer:",
                            q["options"],
                            key=f"answer_{st.session_state.quiz_key}_{i}",
                            index=None
                        )
                    )
                    st.divider()

                submitted = st.form_submit_button("✅ Submit Answers", type="primary")

            if submitted:
                if any(a is None for a in answers):
                    st.warning("Please answer every question before submitting.")
                else:
                    correct = sum(
                        a.strip().lower() == q["answer"].strip().lower()
                        for a, q in zip(answers, questions)
                    )
                    total = len(questions)
                    percentage = correct / total * 100
                    results = [
                        {
                            "question": q["question"],
                            "selected_answer": a,
                            "correct_answer": q["answer"],
                            "correct": a.strip().lower() == q["answer"].strip().lower()
                        }
                        for a, q in zip(answers, questions)
                    ]
                    history.append({
                        "topic": quiz_article["name"],
                        "total_questions": total,
                        "correct_answers": correct,
                        "wrong_answers": total - correct,
                        "score": correct,
                        "percentage": round(percentage, 2),
                        "questions": results
                    })
                    save_history(history)
                    st.session_state.quiz_result = {
                        "topic": quiz_article["name"],
                        "correct": correct,
                        "total": total,
                        "percentage": percentage,
                        "results": results
                    }
                    st.session_state.quiz_submitted = True
                    st.rerun()

        if st.session_state.get("quiz_submitted", False) and "quiz_result" in st.session_state:
            result = st.session_state.quiz_result
            st.success("Quiz submitted successfully!")
            a, b, c = st.columns(3)
            a.metric("Score", f"{result['correct']}/{result['total']}")
            b.metric("Correct Answers", result["correct"])
            c.metric("Percentage", f"{result['percentage']:.1f}%")

            st.progress(result["percentage"] / 100)
            st.subheader("Answer Review")
            for i, item in enumerate(result["results"], 1):
                st.markdown(f"**{i}. {item['question']}**")
                if item["correct"]:
                    st.success(f"Your answer: {item['selected_answer']} ✓")
                else:
                    st.error(f"Your answer: {item['selected_answer']}")
                    st.write(f"Correct answer: {item['correct_answer']}")

            if st.button("🔄 Take Another Quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.pop("quiz_questions", None)
                st.session_state.pop("quiz_result", None)
                st.rerun()

elif page == "📚 Quiz History":
    st.subheader("📚 Your Quiz History")
    if not history:
        st.info("No quizzes completed yet. Start a quiz to see your history here.")
    else:
        for i, h in enumerate(reversed(history), 1):
            total = int(h.get("total_questions", h.get("total", 0)))
            correct = int(h.get("correct_answers", h.get("correct", h.get("score", 0))))
            pct = float(h.get("percentage", correct / total * 100 if total else 0))
            with st.expander(f"{i}. {h.get('topic', 'Unknown Topic')} — {pct:.1f}%"):
                st.write(f"Score: {correct}/{total}")
                st.write(f"Correct: {correct} | Wrong: {total - correct}")
                for j, item in enumerate(h.get("questions", []), 1):
                    if isinstance(item, dict) and "selected_answer" in item:
                        st.write(f"{j}. {item.get('question', '')}")
                        st.write(f"Your answer: {item.get('selected_answer', '')}")
                        st.write(f"Correct answer: {item.get('correct_answer', '')}")

elif page == "📊 Performance":
    st.subheader("📊 Performance Summary")
    if not history:
        st.info("Complete your first quiz to view performance statistics.")
    else:
        total_quizzes = len(history)
        total_questions = sum(int(h.get("total_questions", h.get("total", 0))) for h in history)
        total_correct = sum(int(h.get("correct_answers", h.get("correct", h.get("score", 0)))) for h in history)
        total_wrong = total_questions - total_correct
        overall = total_correct / total_questions * 100 if total_questions else 0

        a, b, c, d = st.columns(4)
        a.metric("Quizzes", total_quizzes)
        b.metric("Questions", total_questions)
        c.metric("Correct", total_correct)
        d.metric("Wrong", total_wrong)

        st.metric("Overall Accuracy", f"{overall:.1f}%")
        st.progress(overall / 100)

        st.markdown("### Quiz-wise Scores")
        chart_data = {
            h.get("topic", f"Quiz {i + 1}"): float(
                h.get("percentage", 0)
            )
            for i, h in enumerate(history)
        }
        st.bar_chart(chart_data)
