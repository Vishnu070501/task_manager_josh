from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Task, UserTask
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

        assigned_users = []
        for user in users:
            # Check if user already has an active assignment for this task
            user_task = UserTask.objects.filter(user=user, task=task).exclude(status='completed').first()
            
            if user_task:
                return Response({
                    "success": False,
                    "status": 400,
                    "message": f"User {user.email} is already assigned to this task and hasn't completed it yet."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new UserTask entry
            UserTask.objects.create(
                user=user,
                task=task,
                status='open'
            )
            assigned_users.append(user.email)

        # You'll need to update the TaskSerializer to work with the new model structure
        # For now, returning basic task info and assigned users
        return Response({
            "success": True,
            "status": 200,
            "message": "Task assigned successfully",
            "data": {
                "task_id": task.id,
                "task_name": task.name,
                "assigned_users": assigned_users
            }
        }, status=status.HTTP_200_OK)

class UserTasks(APIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    permission_codename = 'fetch_task'
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            user_id = request.user.id

        try:
            user = get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return Response({
                "success": False,
                "status": 404,
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Get all UserTask entries for this user
        user_tasks = UserTask.objects.filter(user=user).select_related('task')
        
        # Format the response data
        tasks_data = []
        for user_task in user_tasks:
            task_data = {
                "id": user_task.task.id,
                "name": user_task.task.name,
                "description": user_task.task.description,
                "created_at": user_task.task.created_at,
                "task_type": user_task.task.task_type,
                "is_active": user_task.task.is_active,
                # UserTask specific fields
                "status": user_task.status,
                "assigned_at": user_task.assigned_at,
                "completed_at": user_task.completed_at
            }
            tasks_data.append(task_data)
            
        return Response({
            "success": True,
            "status": 200,
            "message": "Tasks fetched successfully",
            "data": tasks_data
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
                
class UpdateUserTaskStatus(APIView):
    permission_classes = [IsAuthenticated]
    permission_codename = 'update_user_task_status'
    @transaction.atomic
    def put(self, request):
        task_id = request.query_params.get('task_id')
        new_status = request.data.get('status')
        
        if not task_id:
            return Response({
                "success": False,
                "status": 400,
                "message": "Task ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not new_status:
            return Response({
                "success": False,
                "status": 400,
                "message": "New status is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Validate status value
        valid_statuses = [status_choice[0] for status_choice in UserTask.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({
                "success": False,
                "status": 400,
                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Get the user task assignment - specifically for the current user
            user_task = UserTask.objects.get(
                user=request.user,  # Ensures the task is assigned to the current user
                task_id=task_id
            )
        except UserTask.DoesNotExist:
            return Response({
                "success": False,
                "status": 404,
                "message": "Task not assigned to you or not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if task is already completed
        if user_task.status == 'completed':
            return Response({
                "success": False,
                "status": 400,
                "message": "Cannot change status of a completed task"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Validate logical status transitions
        if user_task.status == 'open' and new_status not in ['in_progress', 'blocked']:
            return Response({
                "success": False,
                "status": 400,
                "message": "Open tasks can only be moved to 'in_progress' or 'blocked'"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if user_task.status == 'blocked' and new_status not in ['in_progress', 'open']:
            return Response({
                "success": False,
                "status": 400,
                "message": "Blocked tasks can only be moved to 'in_progress' or 'open'"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if user_task.status == 'in_progress' and new_status not in ['completed', 'blocked']:
            return Response({
                "success": False,
                "status": 400,
                "message": "In-progress tasks can only be moved to 'completed' or 'blocked'"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Update the status
        user_task.status = new_status
        
        # If status is changed to completed, update completed_at timestamp
        if new_status == 'completed':
            from django.utils import timezone
            user_task.completed_at = timezone.now()
            
        user_task.save()
        
        # Prepare response data
        response_data = {
            "task_id": user_task.task.id,
            "task_name": user_task.task.name,
            "status": user_task.status,
            "assigned_at": user_task.assigned_at,
            "completed_at": user_task.completed_at
        }
        
        return Response({
            "success": True,
            "status": 200,
            "message": "Task status updated successfully",
            "data": response_data
        }, status=status.HTTP_200_OK)
