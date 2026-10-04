# AI Counselling Chatbot

A Streamlit campus counsellor that answers student questions with practical guidelines using:

1. Local campus knowledge (TF-IDF retrieval)
2. Web research (DuckDuckGo)
3. Optional Google Gemini API for personalized step-by-step advice

## Features

- Conversational counselling UI
- Career, internship, placement and study guidance
- Expanded college FAQ knowledge base
- Google Gemini integration (optional API key)
- Web research fallback when no API key is set
- Student profile personalization
- Responsible-AI safety escalation for distress keywords

## Run on Windows

1. Install Python 3.10+.
2. Open this folder in VS Code / Cursor.
3. Open Terminal and run:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app/main.py
```

4. Open the URL shown by Streamlit (usually `http://localhost:8501`).

> Note: On Windows PowerShell, `venv\Scripts\activate` may fail due to execution policy.
> Use the `.\venv\Scripts\python.exe -m ...` commands above instead.

## Enable Google Gemini (recommended)

1. Create a free API key at [Google AI Studio](https://aistudio.google.com/apikey).
2. In the app sidebar, paste the key into **Gemini API key**.
3. Keep **Use Google Gemini when available** turned on.

You can also set an environment variable before launching:

```powershell
$env:GEMINI_API_KEY="your_key_here"
streamlit run app/main.py
```

Without a key, the chatbot still answers using the campus knowledge base and web research.

## If `python` does not work

```powershell
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app/main.py
```

## Project structure

```text
AI_Counselling_Chatbot/
├── app/
│   ├── main.py
│   ├── chatbot.py
│   ├── llm.py
│   ├── web_search.py
│   ├── retriever.py
│   ├── safety.py
│   └── __init__.py
├── data/
│   └── knowledge.json
├── requirements.txt
└── README.md
```

# 🤖 AI Counselling Chatbot

An AI-powered counselling chatbot designed to provide personalized, interactive, and supportive guidance to users through natural language conversations.

### 🚀 Key Features

* 💬 Interactive AI-based counselling conversation
* 🧠 Natural Language Processing for understanding user queries
* 🎯 Personalized suggestions based on user needs and interests
* 📚 Career, education, skill-development, and general guidance
* 🔍 Intelligent question-answering and recommendation flow
* 📝 Structured counselling responses and actionable suggestions
* 🖥️ Simple and user-friendly chatbot interface
* 🔐 Designed with responsible and privacy-conscious AI interaction

### 🛠️ Technologies

* Python
* Artificial Intelligence / Generative AI
* Natural Language Processing (NLP)
* Prompt Engineering
* Large Language Models (LLMs)
* Streamlit / Web Interface
* Git & GitHub

### 🎯 Objective

The main objective of this project is to demonstrate how Generative AI can be used to create an intelligent counselling assistant that understands user queries and provides relevant, personalized, and actionable guidance.

### 💡 Use Cases

* Career guidance
* Educational guidance
* Skill and learning recommendations
* Course/technology suggestions
* Personalized career exploration
* AI-based first-level counselling assistance

### 📌 Future Enhancements

* User profile and conversation memory
* Career assessment and recommendation engine
* Resume analysis
* Job-role recommendations
* Voice-based counselling
* Integration with career and course databases
* Advanced analytics dashboard
