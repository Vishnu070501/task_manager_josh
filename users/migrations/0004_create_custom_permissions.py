from django.db import migrations

def create_custom_permissions(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')

    permissions = [
        {'codename': 'create_task', 'name': 'Can create task', 'description': 'Allows creating tasks'},
        {'codename': 'assign_task', 'name': 'Can assign task', 'description': 'Allows assigning tasks to users'},
        {'codename': 'update_task', 'name': 'Can update task', 'description': 'Allows updating tasks'},
        {'codename': 'delete_task', 'name': 'Can delete task', 'description': 'Allows deleting tasks'},
        {'codename': 'fetch_task', 'name': 'Can fetch task', 'description': 'Allows fetching tasks'},
    ]

    for permission_data in permissions:
        CustomPermission.objects.create(**permission_data)

def delete_custom_permissions(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')
    codenames = ['create_task', 'assign_task', 'update_task', 'delete_task', 'fetch_task']
    CustomPermission.objects.filter(codename__in=codenames).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_custompermission_user_custom_permissions'),
    ]

    operations = [
        migrations.RunPython(create_custom_permissions, delete_custom_permissions),
    ] 