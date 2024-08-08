# Generated by Django 5.1 on 2024-08-08 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0005_memo_chat_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memo',
            name='chat_history',
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=10)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_history', to='gpt.memo')),
            ],
        ),
    ]
