from django.urls import path
from .views import CreateTask, AssignTask, UpdateUserTaskStatus, UserTasks, DeleteTask, UpdateTask, FetchAllTasks

urlpatterns = [
    path('create/', CreateTask.as_view(), name='task-create'),
    path('assign/', AssignTask.as_view(), name='task-assign'),
    path('user-tasks/', UserTasks.as_view(), name='user-tasks'),
    path('delete/', DeleteTask.as_view(), name='task-delete'),
    path('update/', UpdateTask.as_view(), name='task-update'),
    path('fetch/', FetchAllTasks.as_view(), name='task-fetch'),
    path('update-my-task-status/', UpdateUserTaskStatus.as_view(), name='update-user-task-status-by-id'),
] 