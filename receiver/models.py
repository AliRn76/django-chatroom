
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Document(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)