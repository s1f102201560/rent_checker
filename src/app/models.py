from django.db import models
from django.urls import reverse
from django.conf import settings

class Resource(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
