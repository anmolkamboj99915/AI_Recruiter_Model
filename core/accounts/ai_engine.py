# ================= AI ENGINE =================

import re
import json
import requests


# ================= CLEAN TEXT =================
def clean_text(text: str) -> str:
    return (text or "").strip()


# ================= SKILL EXTRACTION =================
def extract_skills(text: str):
    text = text.lower()

    skills_db = [
        "python", "django", "react", "javascript",
        "html", "css", "mysql", "node", "express",
        "mongodb", "api", "bootstrap", "jquery"
    ]

    found = []

    for skill in skills_db:
        # ✅ FIX 1: word boundary match
        if re.search(rf'\b{skill}\b', text):
            found.append(skill.capitalize())

    return list(set(found))


# ================= PROJECT PARSER =================
def parse_project(text: str):
    text = clean_text(text).lower()

    tech = extract_skills(text)

    if "dashboard" in text:
        title = "Dashboard Application"
    elif "website" in text:
        title = "Website Project"
    elif "app" in text:
        title = "Application Project"
    else:
        title = "Software Project"

    description = text.capitalize()

    return {
        "title": title,
        "description": description,
        "tech": tech
    }


# ================= EXPERIENCE PARSER =================
def parse_experience(text: str):
    text = clean_text(text)

    # ✅ FIX 2: non-greedy match
    company_match = re.search(r'at\s+([A-Za-z0-9\s]+?)(?:\s|$)', text)
    role_match = re.search(r'as\s+([A-Za-z0-9\s]+?)(?:\s|$)', text)

    company = company_match.group(1) if company_match else "Company"
    role = role_match.group(1) if role_match else "Role"

    return {
        "company": company.strip(),
        "role": role.strip(),
        "description": text,
        "duration": "Not specified"
    }


# ================= SUMMARY GENERATOR =================
def generate_summary(text: str):
    text = clean_text(text)

    if not text:
        return ""

    return text[:200] + ("..." if len(text) > 200 else "")


# ================= RULE-BASED AI =================
def ai_profile_builder(input_text: str):
    text = clean_text(input_text)

    return {
        "summary": generate_summary(text),
        "skills": extract_skills(text),
        "project": parse_project(text),
        "experience": parse_experience(text)
    }


# ================= OLLAMA AI =================
def ollama_ai_profile(text: str):
    prompt = f"""
Convert the following user input into structured JSON.

Input:
{text}

Output format:
{{
    "summary": "...",
    "skills": ["..."],
    "project": {{
        "title": "...",
        "description": "...",
        "tech": ["..."]
    }},
    "experience": {{
        "company": "...",
        "role": "...",
        "description": "...",
        "duration": "..."
    }}
}}

Only return valid JSON.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        if response.status_code != 200:
            raise Exception("Ollama failed")

        data = response.json()
        output = data.get("response", "")

        start = output.find("{")
        end = output.rfind("}") + 1

        if start == -1 or end == 0:
            raise Exception("Invalid JSON from model")

        json_str = output[start:end]

        return json.loads(json_str)

    except Exception:
        return ai_profile_builder(text)