from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Skill, Project
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect


# ================= HELPER =================
def require_login(request):
    return not request.session.get('user_id')


# ================= REGISTER API =================
@api_view(['POST'])
def register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'candidate')

    if not name or not email or not password:
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create(
        name=name,
        email=email,
        password=make_password(password),
        role=role
    )

    return Response({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    })


# ================= LOGIN API =================
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)

        if not check_password(password, user.password):
            return Response({'error': "Invalid credentials"}, status=400)

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        })

    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)


# ================= SAVE PROFILE =================
@api_view(['POST'])
def save_profile(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({"error": "User ID required"}, status=400)

    try:
        user = User.objects.get(id=user_id)

        user.summary = request.data.get('summary', user.summary)
        user.save()

        Skill.objects.filter(user=user).delete()
        Project.objects.filter(user=user).delete()

        for skill in request.data.get('skills', []):
            Skill.objects.create(user=user, name=skill)

        for proj in request.data.get('projects', []):
            Project.objects.create(
                user=user,
                title=proj.get('title'),
                description=proj.get('description'),
                tech=", ".join(proj.get('tech', []))
            )

        return Response({"message": "Profile saved successfully"})

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# ================= AI PARSER =================
def simple_ai_parser(text):
    text = (text or "").lower()

    tech_stack = []

    if "react" in text:
        tech_stack.append("React")
    if "django" in text:
        tech_stack.append("Django")
    if "javascript" in text:
        tech_stack.append("JavaScript")

    title = "Project"
    if "website" in text:
        title = "Website Project"
    elif "app" in text:
        title = "Application Project"

    return {
        "title": title,
        "description": text.capitalize(),
        "tech": tech_stack,
    }


# ================= AI API =================
@api_view(['POST'])
def ai_generate_project(request):
    text = request.data.get("text", "")
    return Response(simple_ai_parser(text))


# ================= GET ALL CANDIDATES =================
@api_view(['GET'])
def get_candidates(request):
    users = User.objects.filter(role='candidate')

    data = []

    for user in users:
        skills = Skill.objects.filter(user=user)
        projects = Project.objects.filter(user=user)

        data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "summary": user.summary,
            "skills": [s.name for s in skills],
            "projects": [
                {
                    "title": p.title,
                    "description": p.description,
                    "tech": p.tech.split(", ")
                }
                for p in projects
            ]
        })

    return Response(data)


# ================= GET SINGLE CANDIDATE =================
@api_view(['GET'])
def get_candidate(request, user_id):
    try:
        user = User.objects.get(id=user_id, role='candidate')
        skills = Skill.objects.filter(user=user)
        projects = Project.objects.filter(user=user)

        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "summary": user.summary,
            "skills": [s.name for s in skills],
            "projects": [
                {
                    "title": p.title,
                    "description": p.description,
                    "tech": p.tech.split(", ")
                }
                for p in projects
            ]
        })

    except User.DoesNotExist:
        return Response({"error": "Candidate not found"}, status=404)


# ================= PAGES =================
def home_page(request):
    return render(request, "accounts/home.html")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['role'] = user.role
                return redirect('/dashboard/')

        except User.DoesNotExist:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


def register_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "candidate")

        if not name or not email or not password:
            return render(request, "accounts/register.html", {"error": "All fields required"})

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {"error": "User already exists"})

        User.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            role=role
        )

        return redirect('/login/')

    return render(request, "accounts/register.html")


def dashboard_page(request):
    if require_login(request):
        return redirect('/login/')
    return render(request, "accounts/dashboard.html")


def ai_builder_page(request):
    if require_login(request):
        return redirect('/login/')

    result = None

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            result = simple_ai_parser(text)

    return render(request, "accounts/ai_builder.html", {"result": result})


def candidates_page(request):
    if require_login(request):
        return redirect('/login/')

    users = User.objects.filter(role='candidate')

    data = []

    for user in users:
        skills = Skill.objects.filter(user=user)

        data.append({
            "id": user.id,
            "name": user.name,
            "summary": user.summary,
            "skills": [s.name for s in skills]
        })

    return render(request, "accounts/candidates.html", {"candidates": data})


def candidate_detail_page(request, user_id):
    if require_login(request):
        return redirect('/login/')

    try:
        user = User.objects.get(id=user_id, role='candidate')
        skills = Skill.objects.filter(user=user)
        projects = Project.objects.filter(user=user)

        data = {
            "name": user.name,
            "email": user.email,
            "summary": user.summary,
            "skills": [s.name for s in skills],
            "projects": [
                {
                    "title": p.title,
                    "description": p.description,
                    "tech": p.tech
                }
                for p in projects
            ]
        }

        return render(request, "accounts/candidate_detail.html", {"candidate": data})

    except User.DoesNotExist:
        return redirect('/candidates-page/')


def logout_page(request):
    request.session.flush()
    return redirect('/')