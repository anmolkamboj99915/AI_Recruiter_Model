from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    
    # Profile Fields
    summary = models.TextField(blank=True)
    
    def __str__(self):
        return self.email
    

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech = models.TextField()
    
    def __str__(self):
        return f"{self.title} ({self.user.email})"