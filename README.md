# Margdarshak AI

## 📌 Overview

Margdarshak AI is an AI-powered career and stream recommendation platform developed using **Python**, **Machine Learning**, **MongoDB**, and **Streamlit**.

The application helps students identify the most suitable academic stream based on:

- Academic performance
- Subject-wise marks
- Personal interests
- Skills and strengths
- Career preferences

Currently, the system is designed primarily for **Class 10 students** who are selecting their stream for higher secondary education. Future updates will expand support for **Class 12 students**, **college recommendations**, **skill assessments**, and **advanced career guidance**.

---

## 🚀 Live Project

🔗 https://margdarshakaii.streamlit.app/

---

## 🎯 Problem Statement

Many students choose streams based on peer pressure, trends, or incomplete information. This often leads to confusion and dissatisfaction later in their academic journey.

**Margdarshak AI** aims to solve this problem by providing data-driven and AI-assisted stream recommendations.

---

## ✨ Features

### 👤 User Management

- User Registration
- Secure Login System
- Profile Management
- Password Update
- Profile Photo Upload

### 🤖 AI-Based Stream Recommendation

The recommendation system uses three independent prediction models:

#### 1️⃣ Interest Analysis Model

Analyzes the student's career goals and interests entered as text.

**Algorithm Used:**

- CountVectorizer
- Multinomial Naive Bayes

---

#### 2️⃣ Academic Performance Model

Predicts suitable streams using subject-wise marks.

**Subjects Considered:**

- Mathematics
- Science
- Social Science
- English

**Algorithm Used:**

- Random Forest Classifier

---

#### 3️⃣ Preference Analysis Model

Evaluates:

- Mathematics Interest
- Science Interest
- Business Interest
- Creativity
- Stress Handling Ability

**Algorithm Used:**

- Random Forest Classifier

---

## 🧠 Final Recommendation Engine

The final stream recommendation is generated using a **Majority Voting System**.

```text
Final Recommendation =
Most Common Prediction among:

1. Interest Model
2. Marks Model
3. Preference Model

---

🛠 Technologies Used

Frontend

- Streamlit

Backend

- Python

Database

- MongoDB Atlas

Data Processing

- Pandas

Machine Learning

- Scikit-Learn

Visualization

- Matplotlib

---

📂 Project Structure

MargdarshakAI/
│
├── MargdarshakAi.py
├── pages/
│   └── Dashboard.py
│
├── images/
│   ├── user_photos/
│   └── updateImg/
│
├── background_img/
│   └── bg.png
│
├── Stream1.csv
├── StudentMark.csv
├── Preference.csv
│
├── requirements.txt
└── README.md

---

⚙️ Machine Learning Workflow

Interest Prediction

Student Goal Text
        ↓
CountVectorizer
        ↓
MultinomialNB
        ↓
Predicted Stream

Marks Prediction

Student Marks
        ↓
Random Forest
        ↓
Predicted Stream

Preference Prediction

Interest Sliders
        ↓
Random Forest
        ↓
Predicted Stream

Final Decision

Interest Prediction
        ↓
Marks Prediction
        ↓
Preference Prediction
        ↓
Majority Voting
        ↓
Final Stream Recommendation

---

🔐 Database Information

MongoDB is used for storing:

- Username
- Password
- Date of Birth
- Profile Photo

Collection Structure

User
│
└── Info
     ├── Name
     ├── Pass
     ├── DOB
     └── Photo
-----
🔮 Future Enhancements

- Support for Class 12 Students
- College Recommendations
- Career Roadmaps
- AI Career Chatbot
- Deep Learning Models
- Skill Assessment Tests
- Scholarship Suggestions
- Resume Builder
- Personalized Career Reports

##👨‍💻 Developer

Hrithick Kumar

Project Motto

«"**Guiding Students Towards the Right Future with Artificial Intelligence.**"»

#Contact

📧 Email: kumarhrithick369@gmail.com

💻 GitHub: Hrithick-kumar

---

#📜 License

This project is developed for educational and research purposes.
