# ================= UTILS =================

import re


# ================= SAFE SPLIT =================
def split_skills(skills_string):
    """
    Converts comma-separated string into clean list
    """
    if not skills_string:
        return []

    return [
        skill.strip()
        for skill in skills_string.split(",")
        if skill.strip()
    ]


# ================= JOIN SKILLS =================
def join_skills(skills_list):
    """
    Converts list into comma-separated string
    """
    if not skills_list:
        return ""

    return ", ".join(skills_list)


# ================= TEXT CLEANER =================
def clean_text(text):
    """
    Basic text cleaning for AI input
    """
    return (text or "").strip()


# ================= SIMPLE KEYWORD MATCH =================
def contains_keywords(text, keywords):
    text = (text or "").lower()
    return any(k.lower() in text for k in keywords)


# ================= SAFE GET =================
def safe_get(data, key, default=None):
    """
    Safe dictionary access
    """
    return data.get(key, default) if isinstance(data, dict) else default


# ================= EMAIL VALIDATION =================
def is_valid_email(email):
    """
    Basic email validation
    """
    if not email:  # ✅ FIX 1: prevent None crash
        return False

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # ✅ FIX 2: ensure string type
    return re.match(pattern, str(email)) is not None