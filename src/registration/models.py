from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    name = models.CharField('氏名', max_length=100)
    email = models.EmailField('メールアドレス', unique=True)
    phone_number = models.CharField('電話番号', max_length=15)
    address = models.CharField('住所', max_length=255)
    email_confirmed = models.BooleanField(default=False)
    created = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
