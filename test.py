import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_josh.settings')

# Configure Django settings
django.setup()

from django.contrib.auth import get_user_model
from users.models import CustomPermission

User = get_user_model()

try:
    user = User.objects.get(id=1)  # Assuming user ID is 1
    create_task_permission = CustomPermission.objects.get(codename='create_task')

    if create_task_permission in user.custom_permissions.all():
        print("User has create_task permission")
    else:
        print("User does NOT have create_task permission")

except User.DoesNotExist:
    print("User not found")
except CustomPermission.DoesNotExist:
    print("Custom permission not found")