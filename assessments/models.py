from django.db import models
from django.conf import settings
from schools.models import ClassRoom
from subjects.models import Subject
from students.models import Student

class Assessment(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assessments')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role':'TEACHER'}, related_name='assessments')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='assessments')
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'title']

    def __str__(self):
        return f'{self.title} ({self.subject.name})'

class AssessmentResult(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assessment_results')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assessment', 'student')
        ordering = ['student__last_name']

    def __str__(self):
        return f"{self.student} → {self.score}"





# Create your models here.
