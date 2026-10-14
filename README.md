# WIKIQUIZ 🧠

A Python-based web application that generates multiple-choice quizzes from Wikipedia article content using the Wikimedia Foundation's Wikipedia Structured Contents dataset.

## 📌 Project Description

WIKIQUIZ is an interactive quiz application developed using Python and Streamlit. It uses Wikipedia article information to help users learn through multiple-choice questions.

The project was initially explored and tested in a Kaggle Notebook using the Wikipedia Structured Contents dataset.

Users can explore topics, answer quiz questions, view their scores, and track their quiz performance through a simple web interface.

## 🌐 Live Application

**Website:** https://wikiquiz-rakshitha-hm.onrender.com

## ✨ Features

- 📚 Uses Wikipedia article data
- 🔎 Searches for articles by topic keyword
- 🎯 Generates multiple-choice quiz questions
- 🔢 Provides four answer options
- ✅ Checks quiz answers
- 📊 Calculates scores and percentages
- 📝 Maintains quiz history
- 📈 Displays overall performance
- 📋 Shows quiz-wise performance
- 🔢 Displays total questions, correct answers, and wrong answers

## 🛠️ Technologies Used

- **Python** – Application logic
- **Streamlit** – Web interface
- **CSV** – Dataset storage and handling, where applicable
- **Wikimedia Foundation's Wikipedia Structured Contents dataset** – Source of Wikipedia article content
- **Kaggle Notebook** – Dataset exploration and initial testing
- **Render** – Web application deployment

## 🗂️ Project Structure

```text
WIKIQUIZ/
├── app.py
├── wikiquiz.py
├── requirements.txt
├── README.md
└── data/
    └── wikipedia_dataset.csv
```

## 🚀 How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/RakshithaHM-git/WIKIQUIZ.git
   ```

2. Navigate to the project folder:

   ```bash
   cd WIKIQUIZ
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL displayed in the terminal.

## 🎯 Project Objective

To make learning from Wikipedia content more interactive by generating quizzes and helping users review their performance.
