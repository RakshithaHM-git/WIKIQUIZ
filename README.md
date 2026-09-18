# WIKIQUIZ

# WIKIQUIZ

A Python-based quiz application that generates multiple-choice questions from Wikipedia article content using a Kaggle-hosted Wikimedia dataset.

## 📌 Project Description

WIKIQUIZ reads Wikipedia article data from the **Wikipedia Structured Contents** dataset available on Kaggle and uses the article information to create interactive multiple-choice quizzes.

The application allows users to select an article, answer questions, view their scores, and track quiz performance.

## ✨ Features

* 📚 Uses Wikipedia article data from a Kaggle dataset
* 🔎 Search and select articles by topic keyword
* 🎯 Generates multiple-choice quiz questions
* ✅ Checks answers instantly
* 📊 Calculates score and percentage
* 📝 Stores quiz history
* 📈 Displays overall performance
* 📋 Displays quiz-wise performance
* 🔢 Shows total questions, correct answers, wrong answers, and percentage

## 🗂️ Project Structure

```text
WIKIQUIZ/
│
├── wikiquiz.py
├── README.md
│
└── data/
    └── wikipedia_dataset.csv
```

The original Kaggle Parquet dataset is used locally to generate the smaller CSV dataset and is not included in this repository.

## 📊 Dataset

This project uses:

**Wikipedia Structured Contents**

Source: Kaggle – Wikimedia Foundation

The dataset contains structured Wikipedia article information. A portion of the English Wikipedia data was processed locally and converted into a CSV file used by WIKIQUIZ.

Dataset:
https://www.kaggle.com/datasets/wikimedia-foundation/wikipedia-structured-contents

License: CC BY-SA 4.0

## 🛠️ Technologies Used

* Python
* Pandas
* JSON
* CSV
* Kaggle Dataset

## ⚙️ Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd WIKIQUIZ
```

Install the required Python package:

```bash
pip install pandas
```

## ▶️ How to Run

Run the application using:

```bash
python wikiquiz.py
```

The application provides the following options:

```text
1. Start Quiz
2. Quiz History
3. Performance Summary
4. Exit
```

## 🎮 Quiz Flow

1. Start the application.
2. Select an article/topic.
3. Read the displayed article content.
4. Answer the multiple-choice questions.
5. View the quiz result.
6. Check quiz history.
7. View quiz-wise and overall performance.

## 📈 Performance Tracking

WIKIQUIZ records quiz performance including:

* Total questions
* Correct answers
* Wrong answers
* Score
* Percentage
* Quiz-wise performance
* Overall performance

Example:

```text
Quiz 1: 1912 Columbus Panhandles season
  Total Questions : 4
  Correct Answers : 1
  Wrong Answers   : 3
  Score           : 1/4
  Percentage      : 25.00%

Quiz 2: 1923 Prime Minister Honours
  Total Questions : 5
  Correct Answers : 3
  Wrong Answers   : 2
  Score           : 3/5
  Percentage      : 60.00%
```

## 👩‍💻 Author

**Rakshitha H M**

BE Computer Science & Engineering
Garden City University, Bengaluru
