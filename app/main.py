import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
from app.chatbot import generate_response
from app.safety import assess_message


st.set_page_config(
    page_title="AI Counselling Chatbot",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
    :root {
        --ink: #14323A;
        --muted: #5B7380;
        --teal: #0F766E;
        --teal-deep: #0A5C56;
        --mint: #D8EFEA;
        --sand: #F4F7F6;
        --card: rgba(255,255,255,0.82);
        --line: rgba(20,50,58,0.10);
        --shadow: 0 18px 50px rgba(15, 60, 70, 0.08);
    }

    html, body, [class*="css"]  {
        font-family: "Manrope", sans-serif;
        color: var(--ink);
    }

    .stApp {
        background:
            radial-gradient(1200px 500px at 10% -10%, #c9ebe4 0%, transparent 55%),
            radial-gradient(900px 420px at 95% 0%, #d7e8f5 0%, transparent 50%),
            linear-gradient(180deg, #f7fbfa 0%, #eef4f2 45%, #e8f1ef 100%);
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(232,242,239,0.95) 100%);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: "Fraunces", serif;
        color: var(--ink);
        letter-spacing: -0.02em;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
        max-width: 980px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 28px;
        padding: 1.7rem 1.8rem 1.5rem;
        margin-bottom: 1.1rem;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.88) 0%, rgba(216,239,234,0.72) 55%, rgba(214,232,245,0.55) 100%);
        box-shadow: var(--shadow);
        animation: riseIn 0.55s ease both;
    }

    .hero::before {
        content: "";
        position: absolute;
        right: -40px;
        top: -50px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(15,118,110,0.18), transparent 70%);
        pointer-events: none;
    }

    .brand {
        font-family: "Fraunces", serif;
        font-size: clamp(2rem, 4vw, 2.8rem);
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.05;
        margin: 0;
        color: var(--ink);
    }

    .brand span {
        color: var(--teal);
    }

    .tagline {
        margin: 0.55rem 0 0;
        max-width: 42rem;
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.55;
        font-weight: 500;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 1rem;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: rgba(15,118,110,0.10);
        color: var(--teal-deep);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        border: 1px solid rgba(15,118,110,0.14);
    }

    .chat-shell {
        border: 1px solid var(--line);
        border-radius: 24px;
        background: var(--card);
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow);
        padding: 0.85rem 0.95rem 0.35rem;
        animation: riseIn 0.7s ease both;
    }

    .section-label {
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--teal-deep);
        margin: 0.2rem 0 0.75rem 0.15rem;
    }

    .suggest-caption {
        color: var(--muted);
        font-size: 0.88rem;
        font-weight: 600;
        margin: 0.85rem 0 0.35rem;
    }

    div[data-testid="stChatMessage"] {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 18px;
        padding: 0.35rem 0.2rem;
        margin-bottom: 0.45rem;
        animation: fadeUp 0.35s ease both;
    }

    div[data-testid="stChatMessage"]:nth-child(odd) {
        /* subtle rhythm */
    }

    /* User / assistant bubbles */
    div[data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.72);
        border-color: var(--line);
        padding: 0.7rem 0.85rem;
        box-shadow: 0 8px 24px rgba(15, 60, 70, 0.04);
    }

    [data-testid="stPills"] button {
        border-radius: 999px !important;
        border: 1px solid rgba(15,118,110,0.16) !important;
        background: rgba(255,255,255,0.88) !important;
        color: var(--teal-deep) !important;
        font-weight: 700 !important;
    }

    [data-testid="stPills"] button[aria-checked="true"] {
        background: var(--teal) !important;
        color: white !important;
        border-color: var(--teal) !important;
    }

    [data-testid="stChatInput"] {
        border-radius: 18px !important;
        border: 1px solid var(--line) !important;
        background: rgba(255,255,255,0.92) !important;
        box-shadow: 0 10px 30px rgba(15, 60, 70, 0.06);
    }

    .stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(15,118,110,0.18);
        background: rgba(255,255,255,0.85);
        color: var(--teal-deep);
        font-weight: 700;
        transition: transform 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        background: var(--mint);
        border-color: rgba(15,118,110,0.28);
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(15,118,110,0.12);
    }

    .footer-note {
        margin-top: 0.85rem;
        color: var(--muted);
        font-size: 0.84rem;
        font-weight: 500;
        text-align: right;
    }

    .sidebar-card {
        border: 1px solid var(--line);
        background: rgba(255,255,255,0.72);
        border-radius: 18px;
        padding: 0.85rem 0.9rem;
        margin-bottom: 0.9rem;
    }

    .sidebar-kicker {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--teal);
        margin-bottom: 0.25rem;
    }

    .sidebar-title {
        font-family: "Fraunces", serif;
        font-size: 1.25rem;
        margin: 0;
        color: var(--ink);
    }

    .sidebar-copy {
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.45;
        margin-top: 0.35rem;
    }

    @keyframes riseIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 768px) {
        .hero { padding: 1.25rem 1.15rem; border-radius: 22px; }
        .brand { font-size: 1.85rem; }
        .chat-shell { border-radius: 18px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

QUICK_PROMPTS = [
    "How can I improve my resume?",
    "How do I get an internship?",
    "DSA kaise start karu?",
    "Campus placement plan for final year",
    "Job chahiye kya kru?",
]

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-kicker">Profile</div>
            <p class="sidebar-title">Student setup</p>
            <p class="sidebar-copy">Personalize answers with your course, year and career goal.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    name = st.text_input("Your name", "Student")
    course = st.selectbox(
        "Course",
        ["BTech", "BCA", "MCA", "BSc", "BCom", "BBA", "MBA", "Other"],
    )
    year = st.selectbox(
        "Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year", "Postgraduate"],
    )
    interests = st.text_input("Interests", "AI, coding, problem solving")
    goal = st.text_input("Career goal", "AI Internship")

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-kicker">AI engine</div>
            <p class="sidebar-title">Gemini boost</p>
            <p class="sidebar-copy">Optional free API key for deeper ChatGPT-style answers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("[Get free Gemini API key](https://aistudio.google.com/apikey)")
    default_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API key",
        value=default_key,
        type="password",
        placeholder="Paste key for richer answers",
        help="Get a free key from Google AI Studio",
    )
    use_ai = st.toggle("Use Google Gemini", value=True)
    if use_ai and not (api_key or "").strip():
        st.caption("No key yet — campus knowledge + web research still work.")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.info(
        "For distress or crisis situations, contact a qualified human counsellor."
    )

st.markdown(
    """
    <section class="hero">
        <h1 class="brand">Campus <span>Counsellor</span></h1>
        <p class="tagline">
            Practical career and study guidance for students — in Hindi or English.
            Built with campus knowledge, web research, and optional Google Gemini.
        </p>
        <div class="pill-row">
            <span class="pill">Career guidance</span>
            <span class="pill">Resume & interviews</span>
            <span class="pill">Internships</span>
            <span class="pill">Placement prep</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.session_state.messages.append(
        (
            "assistant",
            f"Hi {name}! I'm your Campus Counsellor. "
            "Ask about careers, jobs, internships, resumes, interviews, DSA, or studies — "
            "and I'll give a clear step-by-step plan.",
        )
    )

for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

st.markdown(
    '<p class="suggest-caption">Try a quick question</p>',
    unsafe_allow_html=True,
)

selected = st.pills(
    "Quick prompts",
    QUICK_PROMPTS,
    selection_mode="single",
    label_visibility="collapsed",
    key="quick_prompt_pill",
)

prompt = st.chat_input(
    "Ask anything: resume, internship, DSA, placement, career..."
)

active_prompt = None
if prompt:
    active_prompt = prompt
elif selected and selected != st.session_state.get("_last_quick_prompt"):
    active_prompt = selected
    st.session_state._last_quick_prompt = selected

if active_prompt:
    st.session_state.messages.append(("user", active_prompt))

    safety = assess_message(active_prompt)

    if safety["flag"]:
        response = safety["message"]
    else:
        profile = {
            "name": name,
            "course": course,
            "year": year,
            "interests": interests,
            "goal": goal,
        }
        key_to_use = api_key if use_ai else ""
        with st.spinner("Preparing your guidelines..."):
            response = generate_response(active_prompt, profile, api_key=key_to_use)

    st.session_state.messages.append(("assistant", response))
    st.rerun()

foot1, foot2 = st.columns([1, 2])
with foot1:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state._last_quick_prompt = None
        st.rerun()
with foot2:
    st.markdown(
        '<p class="footer-note">Responsible AI · Campus knowledge · Gemini / web research</p>',
        unsafe_allow_html=True,
    )
