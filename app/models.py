from django.db import models

class Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, default="")
    file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
