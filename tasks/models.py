from django.db import models
from django.conf import settings

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('errand', 'Errand'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked','Blocked')
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=100, choices=TASK_TYPE_CHOICES, blank=True, null=True)
    # completed_at = models.DateTimeField(blank=True, null=True)
    # status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    # assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 
    
class UserTask(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked','Blocked')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='user_tasks')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # class Meta:
    #     unique_together = ['user', 'task']  # Each user can have only one relationship with a task
        
    def __str__(self):
        return f"{self.user.email} - {self.task.name} - {self.status}"