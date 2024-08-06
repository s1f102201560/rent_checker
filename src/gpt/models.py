from django.db import models
from django.urls import reverse
from django.conf import settings

class Memo(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gpt:detail', kwargs={'pk': self.pk})

    # 生成系AIの解説を保存
    explanation = models.TextField(blank=True, null=True)
