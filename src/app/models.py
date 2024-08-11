from django.db import models
from pgvector.django import VectorField

class Resource(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField()
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def update_embedding(self, embedding):
      self.embedding = embedding
      self.save()
