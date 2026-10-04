import re

HIGH_RISK = [
    r"\bsuicide\b",
    r"\bkill myself\b",
    r"\bwant to die\b",
    r"\bend my life\b",
    r"\bself[- ]?harm\b",
    r"\bhurt myself\b"
]

DISTRESS = [
    r"\bhopeless\b",
    r"\bpanic\b",
    r"\bvery anxious\b",
    r"\bcan't cope\b",
    r"\bburned out\b"
]


def assess_message(text):
    text = text.lower()

    if any(re.search(pattern, text) for pattern in HIGH_RISK):
        return {
            "level": "HIGH",
            "flag": True,
            "message": (
                "This message may indicate an immediate safety concern. "
                "The chatbot should not handle this alone. Please contact "
                "a trusted person, your college counsellor, or appropriate "
                "local emergency/crisis support now."
            )
        }

    if any(re.search(pattern, text) for pattern in DISTRESS):
        return {
            "level": "MODERATE",
            "flag": True,
            "message": (
                "It sounds like you may be experiencing significant distress. "
                "Consider speaking with your college counsellor, a trusted "
                "person, or a qualified mental-health professional."
            )
        }

    return {
        "level": "LOW",
        "flag": False,
        "message": ""
    }
