# Generated by Django 5.1.7 on 2025-03-24 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': [('create_task', 'Can create task'), ('assign_task', 'Can assign task'), ('update_task', 'Can update task'), ('remove_task', 'Can delete task'), ('fetch_task', 'Can fetch task')]},
        ),
    ]
