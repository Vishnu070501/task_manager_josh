from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, UserTask

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')  # Include relevant user fields

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'created_at', 'task_type', 'is_active')

class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ('id', 'user', 'task', 'status', 'assigned_at', 'completed_at')

class AssignTaskSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        assigned_users_data = validated_data.pop('assigned_users', [])
        task = Task.objects.create(**validated_data)
        for user in assigned_users_data:
            task.assigned_users.add(user)
        return task

    def update(self, instance, validated_data):
        assigned_users_data = validated_data.pop('assigned_users', None)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.task_type = validated_data.get('task_type', instance.task_type)
        instance.completed_at = validated_data.get('completed_at', instance.completed_at)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if assigned_users_data is not None:
            instance.assigned_users.set(assigned_users_data)

        return instance 