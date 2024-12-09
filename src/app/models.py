from django.db import models
from pgvector.django import VectorField
from django.db import models
from django.contrib.auth import get_user_model

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

class Document(models.Model):
    title = models.CharField("相談名", max_length=256)
    file = models.FileField("書類", upload_to='uploads/', blank=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ChatRoom(models.Model):
    name = models.CharField('Room Name', max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.file.name

class ChatLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_logs')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_logs')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='caht_logs', null=True, blank=True)
    prompt = models.TextField('ユーザーの質問')
    response = models.TextField('ChatGPTの応答')
    created_at = models.DateTimeField('対話日時', auto_now_add=True)

    def __str__(self):
        return f"ChatLog {self.id} for {self.user.username} in {self.room_name} on {self.created_at}"