from django.db import models
from schools.models import ClassRoom
from subjects.models import Subject
from accounts.models import CustomUser

WEEKDAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]

class Schedule(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    time = models.TimeField()

    class Meta:
        unique_together = ['classroom', 'weekday', 'time']
        ordering = ['weekday', 'time']

    def __str__(self):
        return f"{self.classroom.name} - {self.subject.name} on {self.get_weekday_display()} at {self.time}"
