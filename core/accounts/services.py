# ================= SERVICES LAYER =================

from .models import User, Skill, Project, Experience


# ================= PROFILE SAVE SERVICE =================
def save_user_profile(user, data):
    """
    Handles profile saving logic (used in views)
    """

    # Update summary
    user.summary = data.get('summary', user.summary)

    # Clear old data
    Skill.objects.filter(user=user).delete()
    Project.objects.filter(user=user).delete()
    Experience.objects.filter(user=user).delete()

    # Save skills
    for skill in data.get('skills', []):
        if skill:  # ✅ FIX 1: prevent empty entries
            Skill.objects.create(user=user, name=skill)

    # Save projects
    for proj in data.get('projects', []):
        Project.objects.create(
            user=user,
            title=proj.get('title') or "Untitled",
            description=proj.get('description') or "",
            tech=", ".join(proj.get('tech', []))
        )

    # Save experience
    for exp in data.get('experiences', []):
        Experience.objects.create(
            user=user,
            company=exp.get('company') or "Company",
            role=exp.get('role') or "Role",
            description=exp.get('description') or "",
            duration=exp.get('duration') or "Not specified"
        )

    # Calculate completion
    completion = 0
    if user.summary:
        completion += 25
    if data.get('skills'):
        completion += 25
    if data.get('projects'):
        completion += 25
    if data.get('experiences'):
        completion += 25

    user.profile_completed = completion
    user.save()

    return completion


# ================= GET USER PROFILE =================
def get_user_profile(user):
    skills = Skill.objects.filter(user=user)
    projects = Project.objects.filter(user=user)
    experiences = Experience.objects.filter(user=user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "summary": user.summary,
        "skills": [s.name for s in skills],
        "projects": [
            {
                "title": p.title,
                "description": p.description,
                "tech": p.tech.split(", ") if p.tech else []  # ✅ FIX 2
            }
            for p in projects
        ],
        "experiences": [
            {
                "company": e.company,
                "role": e.role,
                "description": e.description,
                "duration": e.duration
            }
            for e in experiences
        ]
    }


# ================= GET ALL CANDIDATES =================
def get_all_candidates():
    users = User.objects.filter(role='candidate')

    return [get_user_profile(user) for user in users]