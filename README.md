# 🎤 VoiceQuery AI — LLM-Powered Voice SQL Analytics Assistant

## 📌 Project Overview

**VoiceQuery AI** is an end-to-end Generative AI application that enables users to analyze structured datasets using natural voice or text queries.

The system converts spoken language into SQL queries using a Large Language Model (LLM), executes them on a database, and returns insights in both text and voice.

This project demonstrates how AI can make data analytics accessible to non-technical users.

---

## 🚀 Live Demo

🔗 Try the deployed application here:  
👉 **https://voicequery-aigit-6thngvcar3nfvgaeihsvew.streamlit.app**

---

## 🎯 Problem Statement

Organizations generate massive amounts of data, but most business users cannot extract insights because:

- Requires SQL or technical expertise  
- Dependence on data analysts  
- Slow decision-making  
- Limited access for non-technical teams  

👉 Valuable insights remain locked inside databases.

---

## 💡 Solution

VoiceQuery AI provides a natural language interface for data analytics.

Users can simply speak or type a question, and the system returns relevant insights instantly.

---

## ⚙️ System Workflow

Voice/Text → LLM → SQL Query → Database → Insights → Voice/Text Output

---

## 🚀 Key Features

- 🎤 Voice-based data querying  
- 💬 Text query support  
- 🧠 LLM-powered natural language to SQL conversion  
- 📊 Real-time analytics on structured data  
- 🔊 Text-to-speech responses  
- 🖥️ Interactive Streamlit web interface  
- 🌐 Fully deployed web application  

---

## 📊 Demo Dataset

The prototype is demonstrated using a **Retail Analytics dataset**, enabling:

- Sales performance analysis  
- Product insights  
- Store-level analytics  
- Revenue and profit metrics  

---

## 🧠 AI Approach

- Uses a Large Language Model (LLM) for text-to-SQL generation  
- Executes generated SQL on a structured database (SQLite)  
- Returns results as text and synthesized speech  

---

## ⚙️ System Architecture

User → Voice/Text Input → LLM → SQL Generator → Database → Results → Voice Output

---

## 🧪 Output

The system returns:

- Generated SQL query  
- Query results  
- Natural language explanation  
- Voice response  

---

## 🧰 Tech Stack

### 🧠 AI & Data

- Python  
- LLM API (Groq / Compatible LLM)  
- SQLite  
- Pandas  

### 🎤 Speech Processing (Local Version)

- SpeechRecognition  
- PyAudio  
- pyttsx3  

### 🌐 Web Application

- Streamlit  

### 🔊 Speech Output

- gTTS (Deployment)  
- pyttsx3 (Local)

---

## 📂 Project Structure

```
voicequery-ai/
│
├── app/
│   ├── ai/
│   │   └── text_to_sql.py        # LLM-based text-to-SQL generation
│   │
│   ├── db/
│   │   └── run_query.py          # Database query execution
│   │
│   ├── voice/
│   │   ├── voice_input.py        # Speech-to-text processing
│   │   ├── voice_output.py       # Text-to-speech generation
│   │   └── __init__.py
│   │
│   ├── backend/
│   │   └── app.py                # Backend orchestration logic
│   │
│   ├── config/
│   │   └── .env                  # API keys and configuration
│   │
│   ├── data/
│   │   └── retail_data.csv       # Demo dataset
│   │
│   ├── database/
│   │   └── retail.db             # SQLite database
│   │
│   ├── frontend/
│   │   ├── streamlit_app.py      # Streamlit user interface
│   │   └── app.txt               # Local audio dependencies
│   │
│   ├── scripts/
│   │   └── create_db.py          # Script to build database from CSV
│   │
│   └── streamlit_mic_recorder/  # Browser mic component
│
├── tests/
│   ├── test_db.py
│   ├── test_pipeline.py
│   ├── test_speak.py
│   ├── test_sql.py
│   └── test_voice.py
│
├── requirements.txt              # Deployment dependencies
├── README.md
└── .gitignore
```

## ▶️ How to Run Locally

### 1️⃣ Clone the Repository

git clone https://github.com/bala-ml/voicequery-ai.git  
cd voicequery-ai  

---

### 2️⃣ Install Dependencies

pip install -r requirements.txt  
pip install -r app.txt  

---

### 3️⃣ Run the Application

streamlit run frontend/streamlit_app.py  

Open in browser:

http://localhost:8501  

---

## 🎤 Local Audio Requirements (app.txt)

For local voice recording and offline speech output:

pyaudio  
pyttsx3  

👉 These packages may not work on cloud deployments.

---

## 🌐 Deployment Notes

Cloud platforms often restrict system-level audio libraries.

### 🔹 For Deployment (Streamlit Cloud)

Use browser-based microphone and online TTS:

- Streamlit microphone component  
- gTTS for speech output  
- Remove PyAudio and pyttsx3  

---

## ☁️ Deployment Platforms

This application can be deployed on:

- Streamlit Community Cloud (Recommended)  
- Hugging Face Spaces  
- Render  
- Any Python-compatible cloud platform  

---

## 💡 Future Improvements

- Support for multiple datasets  
- Role-based analytics  
- Dashboard visualization integration  
- Multilingual voice support  
- Real-time enterprise data integration  
- Fine-tuned domain-specific models  

---

## 👤 Author

**Balaji I**  
🎯 Aspiring Machine Learning Engineer | Data Science & AI  
📍 India  

---

## ⭐ Acknowledgment

This project is developed for educational and portfolio purposes to demonstrate practical applications of Generative AI and LLMs in data analytics.

---

## 📄 app.txt (Local Use Only)

Create a file named **app.txt**:

pyaudio  
pyttsx3  