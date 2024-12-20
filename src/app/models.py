from django.db import models
from pgvector.django import VectorField
from django.db import models
from django.contrib.auth import get_user_model

class Resource(models.Model):
    name = models.CharField(verbose_name="資料名", max_length=255)
    document = models.FileField(verbose_name="資料ファイル", blank=True)
    embedding = VectorField(verbose_name="埋め込み", dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.name
    
    def update_embedding(self, embedding):
        self.embedding = embedding
        self.save()

class ChatRoom(models.Model):
    name = models.CharField(verbose_name="チャット部屋名", max_length=255)
    link = models.URLField(verbose_name="チャットURL")
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="ユーザ",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.name

class File(models.Model):
    file = models.FileField(verbose_name="書類名", upload_to='uploads/')
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    
    def __str__(self):
        return self.file.verbose_name

class ChatLog(models.Model):
    name = models.CharField(verbose_name="チャット履歴名", max_length=255)
    user = models.ForeignKey(get_user_model(), verbose_name="ユーザ", on_delete=models.CASCADE, related_name='chat_logs')
    room = models.ForeignKey(ChatRoom, verbose_name="チャット部屋", on_delete=models.CASCADE, related_name='chat_logs')
    file = models.ForeignKey(File, verbose_name="書類", on_delete=models.CASCADE, related_name='caht_logs', null=True, blank=True)
    prompt = models.TextField(verbose_name='ユーザメッセージ', max_length=1024)
    response = models.TextField(verbose_name='システムメッセージ')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f"ChatLog {self.id} for {self.user.username} in {self.room} on {self.created_at}"
    
class Consultation(models.Model):
    title = models.CharField(verbose_name="相談名", max_length=255)
    room = models.OneToOneField(
        to=ChatRoom,
        verbose_name='チャット部屋',
        on_delete=models.CASCADE,
        related_name='consultation',
    )
    room_link = models.URLField(verbose_name="チャットURL")
    file = models.FileField("書類", upload_to='uploads/', blank=True, null=True)
    checklist = models.JSONField("質問項目", blank=True, null=True)
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="ユーザ",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return self.title