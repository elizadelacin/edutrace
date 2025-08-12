from django.db import models
from django.conf import settings
from students.models import Student
from subjects.models import Subject

User = settings.AUTH_USER_MODEL

class Feedback(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_feedbacks', limit_choices_to={'role': 'TEACHER'})
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedbacks', limit_choices_to={'role': 'PARENT'})
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback by {self.teacher} for {self.parent} about {self.student}"
