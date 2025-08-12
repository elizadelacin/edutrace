from django.db import models
from accounts.models import CustomUser
from students.models import Student
from subjects.models import Subject
from schools.models import ClassRoom
from django.db.models import Q

class SemesterChoices(models.TextChoices):
    FIRST = "1", "Birinci yarımil"
    SECOND = "2", "İkinci yarımil"

class ExamTypeChoices(models.TextChoices):
    MS = "MS", "Kiçik Summativ"
    BS = "BS", "Böyük Summativ"
    YI = "YI", "Yekun İllik"

class DailyAssessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.FloatField()

    class Meta:
        unique_together = ['student', 'subject', 'date']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} - {self.score}"

class ExamAssessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    semester = models.CharField(max_length=1, choices=SemesterChoices.choices)
    exam_type = models.CharField(max_length=2, choices=ExamTypeChoices.choices)
    date = models.DateField()
    score = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'semester', 'exam_type'],
                name='unique_bs_per_semester',
                condition=Q(exam_type='BS')
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam_type} ({self.semester})"
