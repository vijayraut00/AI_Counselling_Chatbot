"""Lightweight web research helpers for student guidelines."""

from __future__ import annotations


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search the web for student-guidance sources. Returns empty list on failure."""
    q = (query or "").strip()
    if not q:
        return []

    search_query = f"{q} student guidelines tips"
    hits = []

    try:
        from ddgs import DDGS

        hits = list(DDGS().text(search_query, max_results=max_results))
    except Exception:
        return []

    results = []
    for item in hits:
        title = (item.get("title") or "").strip()
        body = (item.get("body") or item.get("snippet") or "").strip()
        href = (item.get("href") or item.get("link") or "").strip()
        if title or body:
            results.append({"title": title, "snippet": body, "url": href})
    return results


def format_web_context(results: list[dict], limit: int = 4) -> str:
    if not results:
        return ""

    lines = []
    for i, item in enumerate(results[:limit], start=1):
        title = item.get("title") or "Source"
        snippet = item.get("snippet") or ""
        url = item.get("url") or ""
        lines.append(f"{i}. {title}\n   {snippet}\n   {url}".rstrip())
    return "\n".join(lines)


def format_web_guidelines(results: list[dict], query: str) -> str:
    """Fallback response built from search snippets when no LLM key is set."""
    if not results:
        return (
            "I could not find reliable live web results right now. "
            "Try rephrasing your question, or add a Google Gemini API key in the sidebar "
            "for personalized AI guidelines."
        )

    bullets = []
    sources = []
    for item in results[:4]:
        snippet = (item.get("snippet") or "").strip()
        title = (item.get("title") or "Resource").strip()
        url = (item.get("url") or "").strip()
        if snippet:
            bullets.append(f"- {snippet}")
        if url:
            sources.append(f"- [{title}]({url})")

    body = "\n".join(bullets) if bullets else "- No detailed snippets were returned."
    source_block = "\n".join(sources) if sources else "- No links available."

    return (
        f"Here's a practical AI-style guide for **{query.strip()}**:\n\n"
        f"**Key insights from research**\n{body}\n\n"
        f"**What you should do next**\n"
        f"1. Pick the 2 most relevant points above for your current year/goal.\n"
        f"2. Turn them into a 7-day checklist.\n"
        f"3. Build one proof item (resume bullet, project update, or practice set).\n"
        f"4. Ask a mentor to review and improve.\n\n"
        f"**Sources**\n{source_block}"
    )
