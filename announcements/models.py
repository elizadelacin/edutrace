from django.db import models
from accounts.models import CustomUser

class Announcement(models.Model):
    TARGET_CHOICES = [
        ('ALL', 'All Users'),
        ('TEACHERS', 'Only Teachers'),
        ('PARENTS', 'Only Parents'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    target_group = models.CharField(max_length=20, choices=TARGET_CHOICES, default='ALL')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='announcements')

    def __str__(self):
        return self.title
