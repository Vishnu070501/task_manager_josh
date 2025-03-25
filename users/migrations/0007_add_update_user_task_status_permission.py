from django.db import migrations

def create_update_user_task_status_permission(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')

    permission_data = {
        'codename': 'update_user_task_status',
        'name': 'Can update user task status',
        'description': 'Allows updating the status of a task assigned to a user',
    }

    CustomPermission.objects.create(**permission_data)

def delete_update_user_task_status_permission(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')
    CustomPermission.objects.filter(codename='update_user_task_status').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_my_field'),
    ]

    operations = [
        migrations.RunPython(create_update_user_task_status_permission, delete_update_user_task_status_permission),
    ] 