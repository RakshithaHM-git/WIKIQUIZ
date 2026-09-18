import csv
import json
import os
import random
import re

# ============================================================
#                    WIKIQUIZ
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "wikipedia_dataset.csv")
HISTORY_FILE = os.path.join(BASE_DIR, "data", "quiz_history.json")

QUIZ_QUESTIONS = 5


# ============================================================
#                         COLORS
# ============================================================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"


def color(text, colour):
    return f"{colour}{text}{Colors.RESET}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ============================================================
#                         DISPLAY
# ============================================================

def line(char="=", width=70):
    print(char * width)


def title(text):
    print()
    line("=")
    print(color(text.center(70), Colors.BOLD + Colors.CYAN))
    line("=")


def pause():
    input(color("\nPress Enter to continue...", Colors.YELLOW))


# ============================================================
#                    DATASET FUNCTIONS
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    value = str(value)

    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("\\n", " ")
    value = value.replace("\n", " ")
    value = value.replace("\r", " ")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def load_dataset():
    if not os.path.exists(DATA_FILE):
        print(color("\nERROR: Dataset file not found!", Colors.RED))
        print()
        print("Expected file:")
        print(DATA_FILE)
        return []

    articles = []

    try:
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = clean_text(row.get("name", ""))
                description = clean_text(row.get("description", ""))
                abstract = clean_text(row.get("abstract", ""))
                url = clean_text(row.get("url", ""))

                if not name:
                    continue

                content = description

                if len(content) < 80:
                    content = abstract

                if not content:
                    content = abstract

                if content:
                    articles.append({
                        "name": name,
                        "description": description,
                        "abstract": abstract,
                        "content": content,
                        "url": url
                    })

        return articles

    except Exception as error:
        print(color("\nERROR while loading dataset:", Colors.RED))
        print(error)
        return []


# ============================================================
#                    HISTORY FUNCTIONS
# ============================================================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

    except OSError as error:
        print(color("\nCould not save quiz history:", Colors.RED))
        print(error)


# ============================================================
#                 HISTORY COMPATIBILITY
# ============================================================

def get_total_questions(quiz):
    return int(
        quiz.get(
            "total_questions",
            quiz.get(
                "total",
                len(quiz.get("questions", []))
            )
        )
    )


def get_correct_answers(quiz):
    return int(
        quiz.get(
            "correct_answers",
            quiz.get(
                "correct",
                quiz.get("score", 0)
            )
        )
    )


def get_wrong_answers(quiz):
    total = get_total_questions(quiz)
    correct = get_correct_answers(quiz)

    return int(
        quiz.get(
            "wrong_answers",
            quiz.get(
                "wrong",
                max(0, total - correct)
            )
        )
    )


def get_score(quiz):
    return int(
        quiz.get(
            "score",
            get_correct_answers(quiz)
        )
    )


def get_percentage(quiz):
    total = get_total_questions(quiz)

    if total == 0:
        return 0.0

    return float(
        quiz.get(
            "percentage",
            (get_correct_answers(quiz) / total) * 100
        )
    )


# ============================================================
#                     SENTENCE FUNCTIONS
# ============================================================

def get_sentences(text):
    text = clean_text(text)

    sentences = re.split(r"(?<=[.!?])\s+", text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) >= 30
    ]

    return sentences


# ============================================================
#                   DISTRACTOR FUNCTIONS
# ============================================================

def get_distractors(correct_article, articles, count=3):
    correct_name = correct_article["name"]

    candidates = []

    for article in articles:
        name = article["name"]

        if name == correct_name:
            continue

        if name not in candidates:
            candidates.append(name)

    random.shuffle(candidates)

    return candidates[:count]


# ============================================================
#                  QUESTION GENERATION
# ============================================================

def generate_questions(article, articles, number=QUIZ_QUESTIONS):
    questions = []

    title_name = article["name"]
    content = article["content"]

    sentences = get_sentences(content)

    # --------------------------------------------------------
    # Question type 1:
    # What is the article mainly about?
    # --------------------------------------------------------

    questions.append({
        "question": "What is this article mainly about?",
        "options": [
            title_name,
            "A type of computer hardware",
            "A programming language",
            "A mathematical formula"
        ],
        "answer": title_name
    })

    # --------------------------------------------------------
    # Question type 2:
    # Article identification
    # --------------------------------------------------------

    if len(sentences) >= 1:

        sentence = sentences[0]

        if len(sentence) > 180:
            sentence = sentence[:180].rsplit(" ", 1)[0] + "."

        distractors = get_distractors(article, articles, 3)

        if len(distractors) >= 3:
            options = [title_name] + distractors
            random.shuffle(options)

            questions.append({
                "question": (
                    "Which Wikipedia article is associated with "
                    "the following information?\n\n"
                    f"\"{sentence}\""
                ),
                "options": options,
                "answer": title_name
            })

    # --------------------------------------------------------
    # Question type 3:
    # True/False
    # --------------------------------------------------------

    if len(sentences) >= 2:

        sentence = sentences[1]

        if len(sentence) > 180:
            sentence = sentence[:180].rsplit(" ", 1)[0] + "."

        questions.append({
            "question": (
                "According to the selected article, is the "
                "following statement true?\n\n"
                f"\"{sentence}\""
            ),
            "options": [
                "True",
                "False",
                "Cannot be determined",
                "None of the above"
            ],
            "answer": "True"
        })

    # --------------------------------------------------------
    # Question type 4:
    # Description question
    # --------------------------------------------------------

    if len(sentences) >= 3:

        sentence = sentences[2]

        if len(sentence) > 180:
            sentence = sentence[:180].rsplit(" ", 1)[0] + "."

        questions.append({
            "question": (
                "Which statement is directly supported by the "
                "selected Wikipedia article?"
            ),
            "options": [
                sentence,
                "The article is about a programming language.",
                "The article describes a mathematical equation.",
                "The article is about computer hardware."
            ],
            "answer": sentence
        })

    # --------------------------------------------------------
    # Question type 5:
    # Topic question
    # --------------------------------------------------------

    distractors = get_distractors(article, articles, 3)

    if len(distractors) >= 3:

        options = [title_name] + distractors
        random.shuffle(options)

        questions.append({
            "question": (
                "Which topic is most directly connected to "
                "the selected Wikipedia article?"
            ),
            "options": options,
            "answer": title_name
        })

    # Remove duplicate questions
    unique_questions = []
    seen = set()

    for question in questions:
        key = question["question"]

        if key not in seen:
            seen.add(key)
            unique_questions.append(question)

    random.shuffle(unique_questions)

    return unique_questions[:number]


# ============================================================
#                     DISPLAY ARTICLE
# ============================================================

def display_article(article):
    title("SELECTED WIKIPEDIA ARTICLE")

    print(color("Topic:", Colors.YELLOW))
    print(color(article["name"], Colors.BOLD + Colors.GREEN))

    print()

    print(color("Description:", Colors.YELLOW))

    description = article["description"]

    if not description:
        description = article["abstract"]

    if not description:
        description = "No description available."

    print(description)

    print()

    if article["url"]:
        print(color("Source:", Colors.YELLOW))
        print(article["url"])

    line("-")


# ============================================================
#                     SELECT TOPIC
# ============================================================

def select_topic(articles):
    clear_screen()

    title("SELECT WIKIPEDIA TOPIC")

    search = input(
        color(
            "\nEnter a topic keyword (or press Enter for random): ",
            Colors.CYAN
        )
    ).strip()

    if search:
        matches = [
            article
            for article in articles
            if search.lower() in article["name"].lower()
        ]

        if not matches:
            print(color("\nNo matching topic found.", Colors.RED))
            pause()
            return None

        print()

        max_show = min(len(matches), 10)

        for index in range(max_show):
            print(
                color(
                    f"{index + 1}. {matches[index]['name']}",
                    Colors.WHITE
                )
            )

        print()

        while True:
            choice = input(
                color(
                    f"Select topic (1-{max_show}): ",
                    Colors.CYAN
                )
            ).strip()

            if choice.isdigit():
                number = int(choice)

                if 1 <= number <= max_show:
                    return matches[number - 1]

            print(color("Invalid choice. Try again.", Colors.RED))

    else:
        return random.choice(articles)


# ============================================================
#                         RUN QUIZ
# ============================================================

def run_quiz(articles):
    article = select_topic(articles)

    if article is None:
        return

    clear_screen()

    display_article(article)

    print()
    input(
        color(
            "Press Enter to start the quiz...",
            Colors.YELLOW
        )
    )

    questions = generate_questions(
        article,
        articles,
        QUIZ_QUESTIONS
    )

    if not questions:
        print(color("\nUnable to generate questions.", Colors.RED))
        pause()
        return

    correct_answers = 0
    question_results = []

    for index, question in enumerate(questions, start=1):

        clear_screen()

        print()
        line("=")
        print(
            color(
                f"QUESTION {index} OF {len(questions)}".center(70),
                Colors.BOLD + Colors.CYAN
            )
        )
        line("=")

        print()
        print(color(question["question"], Colors.BOLD + Colors.WHITE))
        print()

        options = question["options"]

        # Ensure four options
        options = options[:4]

        for option_index, option in enumerate(options, start=1):
            letter = chr(64 + option_index)

            print(
                color(
                    f"{letter}. {option}",
                    Colors.WHITE
                )
            )

        print()

        valid_letters = [
            chr(65 + i)
            for i in range(len(options))
        ]

        while True:
            answer = input(
                color(
                    "Your answer (A/B/C/D): ",
                    Colors.CYAN
                )
            ).strip().upper()

            if answer in valid_letters:
                break

            print(
                color(
                    "Invalid answer. Please enter A, B, C or D.",
                    Colors.RED
                )
            )

        selected_index = ord(answer) - 65
        selected_answer = options[selected_index]

        correct_answer = question["answer"]

        is_correct = (
            selected_answer.strip().lower()
            == correct_answer.strip().lower()
        )

        if is_correct:
            correct_answers += 1

            print()
            print(
                color(
                    "✓ Correct!",
                    Colors.BOLD + Colors.GREEN
                )
            )

        else:
            print()
            print(
                color(
                    "✗ Incorrect!",
                    Colors.BOLD + Colors.RED
                )
            )

            print(
                color(
                    f"Correct answer: {correct_answer}",
                    Colors.YELLOW
                )
            )

        question_results.append({
            "question": question["question"],
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

        input(
            color(
                "\nPress Enter for the next question...",
                Colors.YELLOW
            )
        )

    # --------------------------------------------------------
    # Calculate result
    # --------------------------------------------------------

    total_questions = len(questions)

    wrong_answers = total_questions - correct_answers

    percentage = (
        (correct_answers / total_questions) * 100
        if total_questions
        else 0
    )

    # --------------------------------------------------------
    # Save history
    # --------------------------------------------------------

    history = load_history()

    quiz_record = {
        "topic": article["name"],
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "total": total_questions,
        "correct": correct_answers,
        "wrong": wrong_answers,
        "score": correct_answers,
        "percentage": round(percentage, 2),
        "questions": question_results
    }

    history.append(quiz_record)

    save_history(history)

    # --------------------------------------------------------
    # Show result
    # --------------------------------------------------------

    clear_screen()

    title("QUIZ RESULT")

    print(
        color(
            f"Topic            : {article['name']}",
            Colors.WHITE
        )
    )

    print(
        color(
            f"Total Questions  : {total_questions}",
            Colors.WHITE
        )
    )

    print(
        color(
            f"Correct Answers  : {correct_answers}",
            Colors.GREEN
        )
    )

    print(
        color(
            f"Wrong Answers    : {wrong_answers}",
            Colors.RED
        )
    )

    print(
        color(
            f"Score            : {correct_answers}/{total_questions}",
            Colors.YELLOW
        )
    )

    print(
        color(
            f"Percentage       : {percentage:.2f}%",
            Colors.BOLD + Colors.CYAN
        )
    )

    print()

    if percentage >= 80:
        print(
            color(
                "Excellent performance!",
                Colors.BOLD + Colors.GREEN
            )
        )
    elif percentage >= 60:
        print(
            color(
                "Good performance!",
                Colors.BOLD + Colors.GREEN
            )
        )
    elif percentage >= 40:
        print(
            color(
                "Keep practicing!",
                Colors.BOLD + Colors.YELLOW
            )
        )
    else:
        print(
            color(
                "More practice recommended.",
                Colors.BOLD + Colors.RED
            )
        )

    pause()


# ============================================================
#                       QUIZ HISTORY
# ============================================================

def show_history():
    clear_screen()

    title("QUIZ HISTORY")

    history = load_history()

    if not history:
        print(
            color(
                "\nNo quiz history available.",
                Colors.YELLOW
            )
        )

        pause()
        return

    for index, quiz in enumerate(history, start=1):

        total = get_total_questions(quiz)
        correct = get_correct_answers(quiz)
        wrong = get_wrong_answers(quiz)
        score = get_score(quiz)
        percentage = get_percentage(quiz)

        topic = quiz.get("topic", "Unknown Topic")

        print()
        print(
            color(
                f"QUIZ {index}",
                Colors.BOLD + Colors.CYAN
            )
        )

        line("-", 70)

        print(f"Topic           : {topic}")
        print(f"Total Questions : {total}")
        print(
            color(
                f"Correct Answers : {correct}",
                Colors.GREEN
            )
        )
        print(
            color(
                f"Wrong Answers   : {wrong}",
                Colors.RED
            )
        )
        print(f"Score           : {score}/{total}")
        print(
            color(
                f"Percentage      : {percentage:.2f}%",
                Colors.YELLOW
            )
        )

    print()
    line("=")

    pause()


# ============================================================
#                  PERFORMANCE SUMMARY
# ============================================================

def show_performance():
    clear_screen()

    title("PERFORMANCE SUMMARY")

    history = load_history()

    if not history:
        print(
            color(
                "\nNo quiz data available yet.",
                Colors.YELLOW
            )
        )

        pause()
        return

    total_quizzes = len(history)

    total_questions = sum(
        get_total_questions(quiz)
        for quiz in history
    )

    total_correct = sum(
        get_correct_answers(quiz)
        for quiz in history
    )

    total_wrong = sum(
        get_wrong_answers(quiz)
        for quiz in history
    )

    total_score = sum(
        get_score(quiz)
        for quiz in history
    )

    overall_percentage = (
        (total_correct / total_questions) * 100
        if total_questions
        else 0
    )

    average_percentage = (
        sum(get_percentage(quiz) for quiz in history)
        / total_quizzes
    )

    # --------------------------------------------------------
    # Overall performance
    # --------------------------------------------------------

    print(
        color(
            "OVERALL PERFORMANCE",
            Colors.BOLD + Colors.MAGENTA
        )
    )

    line("-", 70)

    print(
        f"Total Quizzes       : {total_quizzes}"
    )

    print(
        f"Total Questions     : {total_questions}"
    )

    print(
        color(
            f"Correct Answers     : {total_correct}",
            Colors.GREEN
        )
    )

    print(
        color(
            f"Wrong Answers       : {total_wrong}",
            Colors.RED
        )
    )

    print(
        f"Total Score         : {total_score}/{total_questions}"
    )

    print(
        color(
            f"Overall Percentage  : {overall_percentage:.2f}%",
            Colors.BOLD + Colors.CYAN
        )
    )

    print(
        color(
            f"Average Quiz Score  : {average_percentage:.2f}%",
            Colors.YELLOW
        )
    )

    # --------------------------------------------------------
    # Quiz-wise details
    # --------------------------------------------------------

    print()
    print(
        color(
            "QUIZ-WISE PERFORMANCE",
            Colors.BOLD + Colors.MAGENTA
        )
    )

    line("-", 70)

    for index, quiz in enumerate(history, start=1):

        topic = quiz.get("topic", "Unknown Topic")

        total = get_total_questions(quiz)
        correct = get_correct_answers(quiz)
        wrong = get_wrong_answers(quiz)
        score = get_score(quiz)
        percentage = get_percentage(quiz)

        print()
        print(
            color(
                f"Quiz {index}: {topic}",
                Colors.BOLD + Colors.CYAN
            )
        )

        print(f"  Total Questions : {total}")

        print(
            color(
                f"  Correct Answers : {correct}",
                Colors.GREEN
            )
        )

        print(
            color(
                f"  Wrong Answers   : {wrong}",
                Colors.RED
            )
        )

        print(f"  Score           : {score}/{total}")

        print(
            color(
                f"  Percentage      : {percentage:.2f}%",
                Colors.YELLOW
            )
        )

    print()
    line("=")

    pause()


# ============================================================
#                       MAIN MENU
# ============================================================

def main():

    # Enable UTF-8 console on Windows where possible
    if os.name == "nt":
        os.system("")

    articles = load_dataset()

    if not articles:
        print(
            color(
                "\nNo articles found in the dataset.",
                Colors.RED
            )
        )

        print()
        print(
            "Make sure this file exists:"
        )

        print(DATA_FILE)

        pause()
        return

    while True:

        clear_screen()

        print()
        line("=")
        print(
            color(
                "WIKIQUIZ".center(70),
                Colors.BOLD + Colors.CYAN
            )
        )
        print(
            color(
                "Wikipedia Knowledge Quiz".center(70),
                Colors.MAGENTA
            )
        )
        line("=")

        print()

        print(
            color(
                "1. Start Quiz",
                Colors.GREEN
            )
        )

        print(
            color(
                "2. Quiz History",
                Colors.YELLOW
            )
        )

        print(
            color(
                "3. Performance Summary",
                Colors.MAGENTA
            )
        )

        print(
            color(
                "4. Exit",
                Colors.RED
            )
        )

        print()

        choice = input(
            color(
                "Enter your choice (1-4): ",
                Colors.CYAN
            )
        ).strip()

        if choice == "1":
            run_quiz(articles)

        elif choice == "2":
            show_history()

        elif choice == "3":
            show_performance()

        elif choice == "4":

            clear_screen()

            print()
            line("=")

            print(
                color(
                    "Thank you for using WIKIQUIZ!",
                    Colors.BOLD + Colors.GREEN
                )
            )

            print()

            line("=")

            break

        else:

            print(
                color(
                    "\nInvalid choice. Please enter 1, 2, 3 or 4.",
                    Colors.RED
                )
            )

            pause()


# ============================================================
#                       PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()