from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(verbose_name='氏名', max_length=100)
    email = models.EmailField(verbose_name='メールアドレス', unique=True)
    phone_number = models.CharField(verbose_name='電話番号', max_length=15)
    address = models.CharField(verbose_name='住所', max_length=255)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.username
