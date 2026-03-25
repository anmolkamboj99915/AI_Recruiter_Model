from django.contrib import admin
from .models import User, Skill, Project, Experience, Shortlist


# ================= USER ADMIN =================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'profile_completed')
    search_fields = ('name', 'email')
    list_filter = ('role',)


# ================= SKILL ADMIN =================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)


# ================= PROJECT ADMIN =================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('title',)


# ================= EXPERIENCE ADMIN =================
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'company', 'user')
    search_fields = ('company', 'role')


# ================= SHORTLIST ADMIN =================
@admin.register(Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'recruiter', 'candidate', 'created_at')