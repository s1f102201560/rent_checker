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

from django.db import models
from django.contrib.auth import get_user_model

from django.db import models
from django.contrib.auth import get_user_model

class ChatLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_logs')
    room_name = models.CharField('Room Name', max_length=255)  # ルーム名を保存
    prompt = models.TextField('ユーザーの質問')
    response = models.TextField('ChatGPTの応答')
    created_at = models.DateTimeField('対話日時', auto_now_add=True)

    def __str__(self):
        return f"ChatLog {self.id} for {self.user.username} in {self.room_name} on {self.created_at}"
