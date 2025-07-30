from django.db import models
from accounts.models import CustomUser


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})

    class Meta:
        unique_together = ['name', 'teacher']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.teacher.get_full_name()})"
