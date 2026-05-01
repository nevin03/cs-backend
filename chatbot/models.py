from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=255)
    interest = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.interest}"

class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    step = models.CharField(max_length=50, default="start")
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} - Step: {self.step}"
