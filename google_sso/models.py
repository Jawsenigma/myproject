# models.py
from django.db import models
from django.contrib.auth.models import User

class Essay(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spelling_feedback = models.TextField(null=True, blank=True)
    content_related = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Prompt(models.Model):
    name = models.CharField(max_length=100)
    prompt_text = models.TextField()

    def __str__(self):
        return self.name
