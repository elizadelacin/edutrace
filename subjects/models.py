from django.db import models
from accounts.models import CustomUser

class Subject(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['name']
        ordering = ['name']

    def __str__(self):
        return self.name
