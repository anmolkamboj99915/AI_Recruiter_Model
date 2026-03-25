from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Shortlist
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .services import save_user_profile, get_all_candidates, get_user_profile
from .ai_engine import parse_project, ai_profile_builder, ollama_ai_profile

# ================= HELPER =================
def is_not_logged_in(request):
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

        request.session['user_id'] = user.id
        request.session['role'] = user.role

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
        completion = save_user_profile(user, request.data)

        return Response({
            "completion": completion
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# ================= SHORTLIST ADD =================
@api_view(['POST'])
def add_shortlist(request):
    recruiter_id = request.session.get('user_id')

    # ✅ FIX 1: authentication guard
    if not recruiter_id:
        return Response({"error": "Not authenticated"}, status=401)

    candidate_id = request.data.get('candidate_id')

    try:
        recruiter = User.objects.get(id=recruiter_id, role='recruiter')
        candidate = User.objects.get(id=candidate_id, role='candidate')

        Shortlist.objects.get_or_create(
            recruiter=recruiter,
            candidate=candidate
        )

        return Response({"message": "Added"})

    except User.DoesNotExist:
        return Response({"error": "Invalid user"}, status=400)


# ================= SHORTLIST REMOVE =================
@api_view(['POST'])
def remove_shortlist(request):
    recruiter_id = request.session.get('user_id')

    # ✅ FIX 2: authentication guard
    if not recruiter_id:
        return Response({"error": "Not authenticated"}, status=401)

    candidate_id = request.data.get('candidate_id')

    Shortlist.objects.filter(
        recruiter_id=recruiter_id,
        candidate_id=candidate_id
    ).delete()

    return Response({"message": "Removed"})


# ================= AI API =================
@api_view(['POST'])
def ai_generate_project(request):
    text = request.data.get("text", "")

    if not text:
        return Response({"error": "Text required"}, status=400)

    return Response(parse_project(text))


# ================= GET CANDIDATES =================
@api_view(['GET'])
def get_candidates(request):
    recruiter_id = request.session.get('user_id')

    candidates = get_all_candidates()

    shortlisted_ids = []
    if recruiter_id:
        shortlisted_ids = list(
            Shortlist.objects.filter(recruiter_id=recruiter_id)
            .values_list('candidate_id', flat=True)
        )

    return Response({
        "candidates": candidates,
        "shortlisted": shortlisted_ids
    })


# ================= GET SINGLE CANDIDATE =================
@api_view(['GET'])
def get_candidate(request, user_id):
    try:
        user = User.objects.get(id=user_id, role='candidate')
        return Response(get_user_profile(user))
    except User.DoesNotExist:
        return Response({"error": "Candidate not found"}, status=404)


# ================= ONBOARDING =================
@api_view(['POST'])
def onboarding(request):
    name = request.data.get('name')
    email = request.data.get('email')
    role = request.data.get('role', 'candidate')

    user, _ = User.objects.get_or_create(
        email=email,
        defaults={
            "name": name,
            "password": "",
            "role": role
        }
    )

    # ✅ login after onboarding
    request.session['user_id'] = user.id
    request.session['role'] = user.role

    return Response({"user_id": user.id})


# ================= PAGES =================
def dashboard_page(request):
    if is_not_logged_in(request):
        return redirect('/login/')

    if request.session.get("role") == "recruiter":
        return render(request, "accounts/recruiter_dashboard.html")

    return render(request, "accounts/dashboard.html")


def home_page(request):
    return render(request, "accounts/home.html")


def login_page(request):
    return render(request, "accounts/login.html")


def register_page(request):
    return render(request, "accounts/register.html")


def candidates_page(request):
    if is_not_logged_in(request):
        return redirect('/login/')
    return render(request, "accounts/candidates.html")


def candidate_detail_page(request, user_id):
    if is_not_logged_in(request):
        return redirect('/login/')

    try:
        user = User.objects.get(id=user_id, role='candidate')
        return render(request, "accounts/candidate_detail.html", {
            "candidate": get_user_profile(user)
        })
    except User.DoesNotExist:
        return redirect('/candidates-page/')


def profile_preview_page(request):
    if is_not_logged_in(request):
        return redirect('/login/')
    return render(request, "accounts/profile_preview.html")


def profile_builder_page(request):
    if is_not_logged_in(request):
        return redirect('/login/')
    return render(request, "accounts/profile_builder.html")


def logout_page(request):
    request.session.flush()
    return redirect('/')


def ai_builder_page(request):
    if is_not_logged_in(request):
        return redirect('/login/')
    return render(request, "accounts/ai_builder.html")

@api_view(['POST'])
def ai_generate_profile(request):
    text = request.data.get("text", "")

    if not text:
        return Response({"error": "Text required"}, status=400)

    try:
        # Try AI model first
        data = ollama_ai_profile(text)
    except Exception:
        # fallback
        data = ai_profile_builder(text)

    return Response(data)