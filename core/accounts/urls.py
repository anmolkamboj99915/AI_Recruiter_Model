from django.urls import path
from .views import (
    login, save_profile, ai_generate_project,
    get_candidates, get_candidate,
    ai_builder_page, login_page, candidates_page,
    register, dashboard_page, register_page,
    logout_page, home_page, candidate_detail_page,
    add_shortlist,               
    onboarding,
    profile_preview_page,
    profile_builder_page,
    remove_shortlist,
    ai_generate_profile,
)

urlpatterns = [
    # ================= API ROUTES =================
    path('api/login/', login),
    path('api/profile/save/', save_profile),
    path('api/ai/project/', ai_generate_project),
    path('api/candidates/', get_candidates),
    path('api/candidate/<int:user_id>/', get_candidate),
    path('api/register/', register),
    path('api/shortlist/', add_shortlist),
    path('api/shortlist/remove/', remove_shortlist),
    path('api/onboarding/', onboarding),
    path('api/ai/profile/', ai_generate_profile),

    # ================= PAGE ROUTES =================
    path('', home_page),
    path('login/', login_page),
    path('register/', register_page),
    path('dashboard/', dashboard_page),
    path('ai-builder/', ai_builder_page),
    path('candidates-page/', candidates_page),
    path('candidate/<int:user_id>/', candidate_detail_page),
    path('profile-preview/', profile_preview_page),
    path('logout/', logout_page),
    path('profile-builder/', profile_builder_page),
]