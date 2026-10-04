"""Google Gemini client for student counselling responses."""

from __future__ import annotations

import os


SYSTEM_PROMPT = """You are an expert AI Campus Counsellor for college students — similar to ChatGPT.
Answer ANY student question with clear, complete, practical guidance.

Cover career, jobs, internships, resumes, interviews, DSA, coding, exams, projects,
motivation, higher studies, soft skills and academic doubts.

Style rules:
- Always answer the actual question first (never only greet or list capabilities).
- Use this structure when helpful:
  1) Direct answer
  2) Step-by-step guidelines
  3) Personalized tip using student profile
  4) 7-day action plan
  5) One common mistake to avoid
- If user writes Hindi/Hinglish, reply in clear Hinglish.
- Be specific and actionable, not vague.
- For crisis/self-harm, urge human counsellor / emergency help.
- Do not invent private college policies."""


def _build_user_prompt(message: str, profile: dict, knowledge_context: str, web_context: str) -> str:
    name = profile.get("name", "Student")
    course = profile.get("course", "Not specified")
    year = profile.get("year", "Not specified")
    interests = profile.get("interests", "Not specified")
    goal = profile.get("goal", "Not specified")

    parts = [
        f"Student profile:\n- Name: {name}\n- Course: {course}\n- Year: {year}\n"
        f"- Interests: {interests}\n- Career goal: {goal}",
        f"Student question (answer this directly):\n{message}",
    ]

    if knowledge_context:
        parts.append(
            "Optional campus knowledge notes (use only if relevant):\n"
            f"{knowledge_context}"
        )

    if web_context:
        parts.append(
            "Optional web research snippets (summarize into practical advice):\n"
            f"{web_context}"
        )

    parts.append(
        "Respond like a helpful AI counsellor:\n"
        "1) Direct answer to the question\n"
        "2) Clear step-by-step guidelines\n"
        "3) A short 7-day action plan for this student\n"
        "4) One common mistake to avoid\n"
        "Match the user's language (Hindi/Hinglish/English)."
    )
    return "\n\n".join(parts)


def generate_with_gemini(
    message: str,
    profile: dict,
    api_key: str,
    knowledge_context: str = "",
    web_context: str = "",
    model_name: str = "gemini-2.0-flash",
) -> str | None:
    """Return Gemini counselling reply, or None if the call fails."""
    key = (api_key or os.getenv("GEMINI_API_KEY", "")).strip()
    if not key:
        return None

    try:
        import google.generativeai as genai
    except ImportError:
        return None

    prompt = _build_user_prompt(message, profile, knowledge_context, web_context)
    candidates = [
        model_name,
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro",
    ]

    try:
        genai.configure(api_key=key)
        for name in candidates:
            try:
                model = genai.GenerativeModel(
                    model_name=name,
                    system_instruction=SYSTEM_PROMPT,
                )
                result = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 1200,
                    },
                )
                text = getattr(result, "text", None)
                if text and text.strip():
                    return text.strip()
            except Exception:
                continue
    except Exception:
        return None

    return None
