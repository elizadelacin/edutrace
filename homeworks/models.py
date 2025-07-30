from django.db import models
from schools.models import ClassRoom
from subjects.models import Subject
from accounts.models import CustomUser

class Homework(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='homeworks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['classroom', 'subject', 'title']

    def __str__(self):
        return f"{self.title} - {self.classroom.name} - {self.subject.name}"
