# 🧠 Resume Categorizer using Machine Learning

A machine learning-based resume categorization system with a user-friendly Streamlit interface. Upload a resume (PDF/DOCX), and instantly see the predicted job category. Built to streamline recruitment by automating manual resume sorting.

---

## 📌 Project Overview

This project leverages NLP and ML to categorize resumes into job profiles (e.g., Java Developer, Testing, HR). Designed to eliminate bias and save recruiters hours of manual scanning.

Key objectives:
- Reduce recruiter workload
- Speed up candidate shortlisting
- Maintain fairness via unbiased ML classification

---

## 💡 Features

- 📄 Upload resume (PDF/DOCX) via web UI
- ⚙️ Preprocessing: Clean text, remove noise
- 📊 ML Models: Logistic Regression, SVM, Random Forest
- 📁 Dataset: Kaggle resume datasets (merged and balanced with SMOTE)
- 📉 Analytics: Word clouds, category distributions, model comparison
- 🧪 Evaluation: Accuracy, F1-score, confusion matrix

---

## 📷 Interface Preview

> 🔧 Run `streamlit run application.py` to launch the UI

### 1. 🔐 Upload Page
![Upload Page](./screenshots/login.png)

### 2. 📋 Categorization Output
![User Dashboard](./screenshots/dashboard.png)

### 3. 🧠 Admin Model Summary
![Model Overview](./screenshots/loandetails.png)

---

## 🔬 Model Performance

| Model                 | Accuracy |
|----------------------|----------|
| Logistic Regression  | 87.48%   |
| Random Forest        | 86.95%   |
| SVC                  | 86.49%   |
| KNN                  | 80.73%   |
| Naive Bayes          | 73.25%   |

---

## 🧰 Tech Stack

| Area          | Tools / Libraries                    |
|---------------|---------------------------------------|
| Web UI        | Streamlit                            |
| ML            | scikit-learn, pandas, numpy           |
| NLP           | NLTK, TF-IDF                         |
| Visualization | seaborn, matplotlib                  |
| Data Source   | Kaggle Resume Dataset                |

---

## 📁 Repository Structure

