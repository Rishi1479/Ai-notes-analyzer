from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Section(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Note(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_notes'
    )

    def __str__(self):
        return self.title