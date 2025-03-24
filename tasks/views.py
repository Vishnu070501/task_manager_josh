from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Task
from .serializers import TaskSerializer

class HasCustomPermission(BasePermission):
    def has_permission(self, request, view):
        permission_codename = view.permission_codename
        return request.user.custom_permissions.filter(codename=permission_codename).exists()

class CreateTask(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'create_task'
    @transaction.atomic
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 201,
                "message": "Task created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "status": 400,
                "message": "Something went wrong",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class AssignTask(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'assign_task'
    @transaction.atomic
    def put(self, request):
        task_id = request.query_params.get('task_id')
        user_ids = request.data.get('user_ids')

        if not task_id:
            return Response({
                "success": False,
                "status": 400,
                "message": "Task ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user_ids:
            return Response({
                "success": False,
                "status": 400,
                "message": "User IDs are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id, is_active=True)
        except Task.DoesNotExist:
            return Response({
                "success": False,
                "status": 404,
                "message": "Task not found or is inactive"
            }, status=status.HTTP_404_NOT_FOUND)

        users = get_user_model().objects.filter(id__in=user_ids)
        if len(users) != len(user_ids):
            return Response({
                "success": False,
                "status": 400,
                "message": "One or more users not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        existing_users = task.assigned_users.all()
        for user in users:
            if user not in existing_users:
                task.assigned_users.add(user)
            else:
                raise ValidationError(f"User {user.email} is already assigned to this task.")

        serializer = TaskSerializer(task)
        return Response({
            "success": True,
            "status": 200,
            "message": "Task assigned successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class UserTasks(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'fetch_task'
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({
                "success": False,
                "status": 400,
                "message": "User ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return Response({
                "success": False,
                "status": 404,
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(assigned_users=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Tasks fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class DeleteTask(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'delete_task'
    @transaction.atomic
    def delete(self, request):
        id = request.query_params.get('id')
        if id is None:
            return Response({
                "success":False,
                "status":404,
                "message":"id not provided"
            },status=status.HTTP_404_NOT_FOUND)
        try:
            task = Task.objects.get(id=id, is_active=True)
        except Task.DoesNotExist:
            return Response({
                "success":False,
                "status":404,
                "message":"Task not found"
            },status=status.HTTP_404_NOT_FOUND)
        task.is_active = False
        task.save()
        serializer = TaskSerializer(task)
        return Response({
            "success":True,
            "status":200,
            "message":"Task deleted successfully",
            "data":serializer.data
        },status=status.HTTP_200_OK)

class UpdateTask(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'update_task'
    @transaction.atomic
    def put(self, request):
        id = request.query_params.get('id')
        if id is None:
            return Response({
                "success":False,
                "status":404,
                "message":"id not provided"
            },status=status.HTTP_404_NOT_FOUND)
        try:
            task = Task.objects.get(id=id, is_active=True)
        except Task.DoesNotExist:
            return Response({
                "success":False,
                "status":404,
                "message":"Task not found"
            },status=status.HTTP_404_NOT_FOUND)
        
        update_task = request.data
        serializer = TaskSerializer(task, data=update_task)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success":True,
                "status":200,
                "message":"Task updated successfully",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "success":False,
                "status":400,
                "message":"Something went wrong",
                "data": serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)

class FetchAllTasks(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'fetch_task'
    def get(self,request):
        id = request.query_params.get('id')
        if id is None:
            tasks = Task.objects.filter(assigned_users=request.user, is_active=True)
            serializer = TaskSerializer(tasks,many=True)
            return Response({
                "success":True,
                "status":200,
                "message":"Tasks fetched successfully",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        else:
            try:
                task = Task.objects.get(id=id, is_active=True)
                serializer = TaskSerializer(task)
                return Response({
                    "success":True,
                    "status":200,
                    "message":"Task fetched successfully",
                    "data":serializer.data
                },status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({
                    "success":False,
                    "status":404,
                    "message":"Task not found"
                },status=status.HTTP_404_NOT_FOUND) 