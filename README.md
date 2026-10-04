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

## How responses are built

1. Safety check for distress / crisis language
2. Retrieve related answers from `data/knowledge.json`
3. Gather short web research snippets
4. If Gemini key is present, generate personalized guidelines
5. Otherwise return structured local / web guidance

## Interview explanation

"I built an AI counselling chatbot for college students. It combines TF-IDF knowledge retrieval, web research and optional Google Gemini generation so students get practical step-by-step guidelines. A safety layer escalates sensitive distress cases to human support."
