from django.db import models
from schools.models import ClassRoom
from students.models import Student
from subjects.models import Subject
from accounts.models import CustomUser

class Attendance(models.Model):
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ['student', 'subject', 'classroom', 'date']
