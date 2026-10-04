import re

from .retriever import search_knowledge, reload_knowledge
from .llm import generate_with_gemini
from .web_search import search_web, format_web_context, format_web_guidelines


_QUERY_HINTS = [
    (r"\b(job|naukri|placement|hire|hiring)\b|job chahiye|naukri chahiye|job mil", "how to get a job after college"),
    (r"\binternship\b|internship chahiye|intern chahiye", "how to get an internship for college students"),
    (r"\bresume\b|\bcv\b|resume kaise|improve my resume", "how can I improve my resume for students"),
    (r"\binterview\b|interview tip", "how to prepare for job interview as student"),
    (r"\bcareer\b|career confuse|confused|kya kru|kya karu|kya karna", "career guidance for college students"),
    (r"\bstudy\b|padhai|exam|semester", "study plan and exam preparation tips"),
    (r"\bproject\b|project ideas", "final year project ideas for engineering students"),
    (r"\bdsa\b|data structure|leetcode", "how to start DSA for placements"),
    (r"\bgithub\b|portfolio\b", "how to build github portfolio as student"),
]


def _is_greeting(text: str) -> bool:
    return bool(re.search(r"^\s*(hi|hello|hey|hii|hiii|namaste|namaskar)\b", text))


def _is_thanks(text: str) -> bool:
    return bool(re.search(r"\b(thank|thanks|thx|dhanyavad|shukriya)\b", text))


def _enrich_query(message: str) -> str:
    text = (message or "").lower()
    extras = []
    for pattern, hint in _QUERY_HINTS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            extras.append(hint)
    if not extras:
        return message
    return f"{message}\n\nSearch intent: {'; '.join(dict.fromkeys(extras))}"


def _format_knowledge_context(results: list[dict]) -> str:
    if not results:
        return ""
    chunks = []
    for item in results[:3]:
        chunks.append(
            f"- Topic: {item['topic']}\n"
            f"  Q: {item['question']}\n"
            f"  A: {item['answer']}"
        )
    return "\n".join(chunks)


def _week_plan(topic: str, goal: str) -> list[str]:
    plans = {
        "resume": [
            "Day 1: Rewrite header, education and skills for your target role",
            "Day 2–3: Convert projects into problem–action–result bullets",
            "Day 4: Add GitHub/LinkedIn links and remove weak fluff",
            "Day 5: Tailor one version to a real job description",
            "Day 6: Get mentor/peer feedback and fix ATS formatting",
            "Day 7: Export PDF and start applying with the new resume",
        ],
        "interview": [
            "Day 1: Write self-intro + project stories (STAR)",
            "Day 2–3: Revise core fundamentals for your role",
            "Day 4: Practice 20 common HR + technical questions",
            "Day 5–6: Do 2 mock interviews and note weak answers",
            "Day 7: Revise mistakes and prepare questions for interviewer",
        ],
        "job_search": [
            "Day 1–2: Resume + LinkedIn upgrade",
            "Day 3–4: Polish one flagship project demo",
            "Day 5–6: Send 20+ targeted applications",
            "Day 7: Mock interview + revise weak topics",
        ],
        "internship_search": [
            "Day 1: Shortlist 30 roles matching your skills",
            "Day 2: Customize resume for top 10 roles",
            "Day 3–5: Apply daily and request 5 referrals",
            "Day 6–7: Prepare internship interview answers",
        ],
        "ai": [
            "Day 1–2: Revise Python, SQL and ML basics",
            "Day 3–5: Improve one end-to-end AI project + README",
            "Day 6: Record a 2-minute demo explanation",
            "Day 7: Apply to 10 AI internship roles",
        ],
        "coding_skills": [
            "Day 1–5: Solve 1–2 coding problems daily",
            "Day 3–6: Build or improve one mini-project",
            "Day 7: Refactor code and write a clean README",
        ],
        "dsa": [
            "Day 1–2: Arrays + hashing practice",
            "Day 3–4: Strings + two pointers",
            "Day 5–6: Recursion + linked list basics",
            "Day 7: Revise patterns and timed mixed set",
        ],
        "exam_prep": [
            "Day 1: Syllabus map + weak-chapter list",
            "Day 2–5: Active recall + past paper practice",
            "Day 6: Full timed mock test",
            "Day 7: Revise mistakes and formula sheet",
        ],
    }
    default = [
        f"Day 1: Define one clear outcome related to {goal}",
        "Day 2–3: Learn or improve the most important skill",
        "Day 4–5: Build proof (project, notes, or practice set)",
        "Day 6: Get feedback from a mentor/peer",
        "Day 7: Review progress and plan next week",
    ]
    return plans.get(topic, default)


def _mistake_for(topic: str) -> str:
    mistakes = {
        "resume": "Listing every tool you ever touched without proof — recruiters prefer fewer skills with strong project evidence.",
        "interview": "Memorizing answers without understanding your own projects.",
        "job_search": "Only applying and never improving skills/projects after rejections.",
        "internship_search": "Sending the same generic resume to every role.",
        "ai": "Watching tutorials endlessly without finishing one deployable project.",
        "coding_skills": "Jumping frameworks before learning language fundamentals.",
        "dsa": "Random problem solving with no topic plan or revision.",
        "exam_prep": "Re-reading notes instead of active recall and past papers.",
        "confusion": "Waiting for perfect clarity before taking any small experiment.",
    }
    return mistakes.get(
        topic,
        "Collecting tips endlessly without a weekly action checklist.",
    )


def _ai_style_answer(message: str, profile: dict, results: list[dict]) -> str:
    """Build a ChatGPT-like structured answer from local knowledge."""
    name = profile.get("name", "Student")
    course = profile.get("course", "your course")
    year = profile.get("year", "your year")
    goal = profile.get("goal", "your career goal")
    interests = profile.get("interests", "your interests")

    best = results[0]
    topic = best.get("topic", "career")
    core = best.get("answer", "").strip()
    week = _week_plan(topic, goal)
    week_block = "\n".join(f"- {step}" for step in week)

    related = []
    for item in results[1:3]:
        if item.get("score", 0) < 0.08:
            continue
        related.append(
            f"- **{item['topic'].replace('_', ' ').title()}**: {item['answer']}"
        )
    related_block = "\n".join(related)

    reply = (
        f"Got it, **{name}** — here's a clear plan for your question.\n\n"
        f"**Direct answer**\n{core}\n\n"
        f"**Personalized for you**\n"
        f"As a **{course}** student in **{year}**, aiming for **{goal}** "
        f"(interests: {interests}), prioritize proof that matches your target role: "
        f"skills + projects + a clean application package.\n\n"
        f"**Step-by-step guidelines**\n"
        f"1. Clarify the exact role/outcome you want this month.\n"
        f"2. Apply the advice above to your current resume/projects/study system.\n"
        f"3. Create measurable weekly targets (applications, problems, or project tasks).\n"
        f"4. Review with a mentor and improve based on feedback.\n\n"
        f"**7-day action plan**\n{week_block}\n\n"
        f"**Common mistake to avoid**\n{_mistake_for(topic)}\n"
    )

    if related_block:
        reply += f"\n**Related guidance**\n{related_block}\n"

    reply += (
        f"\n---\n"
        f"_Matched topic: {topic.replace('_', ' ').title()} "
        f"(confidence {best['score']:.2f}). "
        f"Add a Gemini API key in the sidebar for even deeper ChatGPT-style answers._"
    )
    return reply


def _job_hinglish_plan(profile: dict) -> str:
    name = profile.get("name", "Student")
    course = profile.get("course", "your course")
    year = profile.get("year", "your year")
    goal = profile.get("goal", "your career goal")
    interests = profile.get("interests", "your interests")
    return (
        f"**{name}, job ke liye ye practical plan follow karo:**\n\n"
        f"Aap **{course}** ({year}) student ho aur goal **{goal}** hai "
        f"(interests: {interests}).\n\n"
        f"**Direct answer**\n"
        f"Skill + projects + applications teeno parallel chalao. "
        f"Sirf wait mat karo — weekly apply + weekly build routine banao.\n\n"
        f"**Step-by-step guidelines**\n"
        f"1. 1-page resume: skills, 2–3 projects, GitHub/LinkedIn.\n"
        f"2. Ek strong project polish karo.\n"
        f"3. Roz 5–10 roles apply karo (LinkedIn, Naukri, Internshala, careers pages).\n"
        f"4. Aptitude + DSA/core + communication practice.\n"
        f"5. Placement cell + alumni referrals.\n"
        f"6. Weekly mock interview.\n\n"
        f"**7-day starter plan**\n"
        f"- Day 1–2: Resume + LinkedIn\n"
        f"- Day 3–4: Project demo + README\n"
        f"- Day 5–6: 20+ applications\n"
        f"- Day 7: Mock interview + weak topics\n\n"
        f"**Common mistake**\n"
        f"Bina proof ke sirf apply karna. Evidence ke saath apply karo."
    )


def generate_response(message: str, profile: dict, api_key: str = "") -> str:
    reload_knowledge()
    text = (message or "").lower().strip()

    if _is_greeting(text):
        return (
            f"Hi {profile.get('name', 'Student')}! "
            "I'm your AI Campus Counsellor. Ask me anything about career, jobs, "
            "internships, resume, interviews, DSA, projects or studies — "
            "in Hindi or English — and I'll give a proper step-by-step answer."
        )

    if _is_thanks(text):
        return (
            "You're welcome! Keep going consistently. "
            "If you want, ask for a weekly plan next."
        )

    enriched = _enrich_query(message)
    search_text = enriched if enriched != message else message

    knowledge_hits = search_knowledge(search_text, top_k=3)
    if not knowledge_hits or knowledge_hits[0]["score"] < 0.10:
        alt_hits = search_knowledge(message, top_k=3)
        if alt_hits and (not knowledge_hits or alt_hits[0]["score"] > knowledge_hits[0]["score"]):
            knowledge_hits = alt_hits

    strong_local = [r for r in knowledge_hits if r["score"] >= 0.10]
    knowledge_context = _format_knowledge_context(strong_local or knowledge_hits)

    web_results = search_web(search_text, max_results=5)
    if not web_results:
        web_results = search_web(message, max_results=5)
    web_context = format_web_context(web_results)

    ai_reply = generate_with_gemini(
        message=message,
        profile=profile,
        api_key=api_key,
        knowledge_context=knowledge_context,
        web_context=web_context,
    )
    if ai_reply:
        return f"{ai_reply}\n\n---\n_Answered with Google Gemini_"

    wants_job = bool(
        re.search(
            r"\b(job|naukri|placement|hire)\b|job chahiye|naukri chahiye|kya kru|kya karu",
            text,
        )
    )
    # Prefer structured local AI-style answers when we have a decent match
    if strong_local and strong_local[0]["score"] >= 0.12:
        # For Hindi job phrasing, use Hinglish plan if query looks Hinglish
        if wants_job and re.search(r"(chahiye|kya kru|kya karu|naukri)", text):
            return _job_hinglish_plan(profile)
        return _ai_style_answer(message, profile, strong_local)

    if wants_job:
        return _job_hinglish_plan(profile)

    if web_results:
        return format_web_guidelines(web_results, message)

    if knowledge_hits:
        return _ai_style_answer(message, profile, knowledge_hits)

    return (
        f"{profile.get('name', 'Student')}, I understood your question. "
        "For deeper ChatGPT-style answers, add a free Gemini API key in the sidebar "
        "(https://aistudio.google.com/apikey).\n\n"
        f"Meanwhile, as a {profile.get('course', 'student')} in "
        f"{profile.get('year', 'college')} aiming for **{profile.get('goal', 'your goal')}**:\n"
        "1. Write your goal in one sentence.\n"
        "2. Pick 3 tasks for this week.\n"
        "3. Review progress with a mentor."
    )
