# Generated by Django 5.1.4 on 2024-12-21 04:50

import django.db.models.deletion
import pgvector.django.vector
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/', verbose_name='書類名')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='資料名')),
                ('document', models.FileField(blank=True, upload_to='', verbose_name='資料ファイル')),
                ('embedding', pgvector.django.vector.VectorField(blank=True, dimensions=1536, null=True, verbose_name='埋め込み')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='チャット部屋名')),
                ('link', models.URLField(verbose_name='チャットURL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='相談名')),
                ('room_link', models.URLField(verbose_name='チャットURL')),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='書類')),
                ('checklist', models.JSONField(blank=True, null=True, verbose_name='質問項目')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='app.chatroom', verbose_name='チャット部屋')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='チャット履歴名')),
                ('prompt', models.TextField(max_length=1024, verbose_name='ユーザメッセージ')),
                ('response', models.TextField(verbose_name='システムメッセージ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_logs', to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_logs', to='app.chatroom', verbose_name='チャット部屋')),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_logs', to='app.file', verbose_name='書類')),
            ],
        ),
    ]
