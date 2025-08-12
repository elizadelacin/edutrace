from django.db import models
from django.conf import settings

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'TEACHER'},
        related_name='classrooms',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'name')
        ordering = ['school__name', 'name']

    def __str__(self):
        return f"{self.school.name} – {self.name}"

class TeachingAssignment(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='teaching_assignments')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'TEACHER'},
        related_name='teaching_assignments'
    )
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='teaching_assignments')

    class Meta:
        unique_together = ('classroom', 'teacher', 'subject')
        ordering = ['classroom__school__name', 'classroom__name', 'subject__name']

    def __str__(self):
        return f"{self.classroom} - {self.subject.name} - {self.teacher.get_full_name()}"
