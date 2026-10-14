# WIKIQUIZ

A Python-based quiz application that generates multiple-choice questions from Wikipedia article content using the Wikimedia Foundation's Wikipedia Structured Contents dataset.

## 📌 Project Description

WIKIQUIZ is a Python-based quiz application that uses Wikipedia article information to generate multiple-choice questions.

The existing WIKIQUIZ project was integrated and tested in a Kaggle Notebook using the **Wikipedia Structured Contents** dataset provided by the Wikimedia Foundation.

The application allows users to select or use Wikipedia articles, answer quiz questions, receive instant feedback, and track quiz performance.

## ✨ Features

- 📚 Uses Wikipedia article data
- 🔎 Searches and selects articles by topic keyword
- 🎯 Generates multiple-choice quiz questions
- 🔢 Provides four answer options
- ✅ Checks answers instantly
- 📊 Calculates quiz scores and percentages
- 📝 Stores quiz history
- 📈 Displays overall performance
- 📋 Displays quiz-wise performance
- 🔢 Shows total questions, correct answers, wrong answers, and percentage

## 🗂️ Project Structure

```text
WIKIQUIZ/
│
├── wikiquiz.py
├── README.md
│
└── data/
    └── wikipedia_dataset.csv
# WIKIQUIZ 🧠

A Python-based, web-based quiz application that generates multiple-choice questions from Wikipedia article content using the Wikimedia Foundation's Wikipedia Structured Contents dataset.

## 📌 Project Description

WIKIQUIZ is a web-based quiz application developed using Python and Streamlit. It uses Wikipedia article information to create interactive multiple-choice quizzes.

The project uses the **Wikipedia Structured Contents** dataset provided by the Wikimedia Foundation and was initially tested in a Kaggle Notebook.

Users can explore topics, answer quiz questions, view their scores, and track quiz performance through a simple web interface.

## 🌐 Live Application

**Website:** https://wikiquiz-rakshitha-hm.onrender.com

## ✨ Features

- 📚 Uses Wikipedia article data
- 🔎 Searches and selects articles by topic keyword
- 🎯 Generates multiple-choice quiz questions
- 🔢 Provides four answer options
- ✅ Checks quiz answers
- 📊 Calculates scores and percentages
- 📝 Maintains quiz history
- 📈 Displays overall performance
- 📋 Shows quiz-wise performance
- 🔢 Displays total questions, correct answers, wrong answers, and percentage

## 🛠️ Technologies Used

- **Python** – Application logic
- **Streamlit** – Web interface
- **Pandas / CSV** – Dataset handling, where applicable
- **Wikimedia Foundation's Wikipedia Structured Contents dataset** – Source of Wikipedia article content
- **Render** – Web application deployment
- **Kaggle Notebook** – Dataset exploration and initial testing

## 🗂️ Project Structure

```text
WIKIQUIZ/
│
├── app.py
├── wikiquiz.py
├── requirements.txt
├── README.md
│
└── data/
    └── wikipedia_dataset.csv
```

## 🚀 How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/RakshithaHM-git/WIKIQUIZ.git
   ```

2. Open the project folder:

   ```bash
   cd WIKIQUIZ
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL displayed in the terminal.

## 🎯 Project Objective

To make learning from Wikipedia content more interactive by allowing users to practice through automatically generated quizzes and review their performance.

