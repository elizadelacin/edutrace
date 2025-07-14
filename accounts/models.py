from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

def generate_invite_code():
    return get_random_string(32)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('TEACHER', 'Teacher'),
        ('PARENT', 'Parent'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.ForeignKey('schools.School', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    subjects = models.ManyToManyField('subjects.Subject', blank = True, related_name = 'teachers')
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Invitation(models.Model):
    code = models.CharField(max_length=64, unique=True, default=generate_invite_code, editable=False)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='invitations')
    role = models.CharField(max_length=10, choices=CustomUser.ROLE_CHOICES)
    email = models.EmailField()
    used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} invitation for {self.email} ({self.school.name})"
