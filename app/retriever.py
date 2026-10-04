import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).resolve().parents[1]
KNOWLEDGE_PATH = BASE / "data" / "knowledge.json"

KNOWLEDGE = []
VECTORIZER = None
MATRIX = None
_LOADED_MTIME = None


def reload_knowledge(force: bool = False):
    """Reload knowledge.json when the file changes."""
    global KNOWLEDGE, VECTORIZER, MATRIX, _LOADED_MTIME

    mtime = KNOWLEDGE_PATH.stat().st_mtime
    if not force and _LOADED_MTIME == mtime and VECTORIZER is not None:
        return

    with open(KNOWLEDGE_PATH, encoding="utf-8") as f:
        KNOWLEDGE = json.load(f)

    corpus = [
        f"{item['question']} {item['answer']} {item['topic']}"
        for item in KNOWLEDGE
    ]
    VECTORIZER = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    MATRIX = VECTORIZER.fit_transform(corpus)
    _LOADED_MTIME = mtime


reload_knowledge(force=True)


def search_knowledge(query, top_k=3):
    if not query.strip():
        return []

    reload_knowledge()
    query_vector = VECTORIZER.transform([query])
    scores = cosine_similarity(query_vector, MATRIX)[0]
    indices = scores.argsort()[::-1][:top_k]

    results = []
    for i in indices:
        if scores[i] > 0:
            results.append({
                "topic": KNOWLEDGE[i]["topic"],
                "question": KNOWLEDGE[i]["question"],
                "answer": KNOWLEDGE[i]["answer"],
                "score": float(scores[i]),
            })
    return results
