from rest_framework import serializers
from .models import User, Skill, Project


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # ✅ FIX 1: correct related_name usage
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'