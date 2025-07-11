# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ModuleLoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    ip = models.CharField(max_length=39, blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_logged_in = models.BooleanField(default=True)
    module = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} - {self.module} - {self.date_time}"

class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)