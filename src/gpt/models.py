from django.db import models
from django.urls import reverse
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField(max_length=1000)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('gpt:detail', kwargs={'pk': self.pk})