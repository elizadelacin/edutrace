from django.db import models
from django.db.models import Avg
from accounts.models import CustomUser
from students.models import Student
from subjects.models import Subject
from schools.models import ClassRoom

class DailyAssessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    score = models.FloatField()
    note = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

class ExamAssessment(models.Model):
    EXAM_TYPE_CHOICES = [
        ('MS', 'Kiçik Summativ'),
        ('BS', 'Böyük Summativ'),
        ('YI', 'İllik Qiymət'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=2, choices=EXAM_TYPE_CHOICES)
    score = models.FloatField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'subject', 'exam_type']
        ordering = ['-date']
