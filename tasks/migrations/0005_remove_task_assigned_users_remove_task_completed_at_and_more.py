# Generated by Django 5.1.7 on 2025-03-25 15:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_status_alter_task_task_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_users',
        ),
        migrations.RemoveField(
            model_name='task',
            name='completed_at',
        ),
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('blocked', 'Blocked')], default='open', max_length=50)),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
