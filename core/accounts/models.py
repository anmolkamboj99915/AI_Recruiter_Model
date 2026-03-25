from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# ================= USER =================
class User(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    # Profile Fields
    summary = models.TextField(blank=True)
    profile_completed = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']


# ================= SKILL =================
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    class Meta:
        ordering = ['name']


# ================= PROJECT =================
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech = models.TextField()  # Stored as comma-separated values

    def __str__(self):
        return f"{self.title} ({self.user.email})"

    class Meta:
        ordering = ['-id']


# ================= EXPERIENCE =================
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.role} at {self.company} ({self.user.email})"

    class Meta:
        ordering = ['-id']


# ================= SHORTLIST =================
class Shortlist(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortlisted')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recruiter', 'candidate')

    def clean(self):
        # ✅ enforce roles
        if self.recruiter.role != 'recruiter':
            raise ValueError("Recruiter must have recruiter role")

        if self.candidate.role != 'candidate':
            raise ValueError("Candidate must have candidate role")

    def save(self, *args, **kwargs):
        self.clean()  # ✅ enforce validation before save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recruiter.email} → {self.candidate.email}"