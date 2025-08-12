from django.db import models
from django.conf import settings
from schools.models import School, ClassRoom

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, related_name='students')
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'PARENT'},
        related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('first_name', 'last_name', 'classroom')
        ordering = ['school__name', 'classroom__name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()
