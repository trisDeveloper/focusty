from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    done = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title