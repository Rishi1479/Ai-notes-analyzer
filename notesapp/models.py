from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Note(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')

    def __str__(self):
        return self.title