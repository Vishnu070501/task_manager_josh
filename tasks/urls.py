from django.urls import path
from .views import CreateTask, AssignTask, UserTasks, DeleteTask, UpdateTask, FetchAllTasks

urlpatterns = [
    path('create/', CreateTask.as_view(), name='task-create'),
    path('assign/', AssignTask.as_view(), name='task-assign'),
    path('tasks/', UserTasks.as_view(), name='user-tasks'),
    path('delete/', DeleteTask.as_view(), name='task-delete'),
    path('update/', UpdateTask.as_view(), name='task-update'),
    path('fetch/', FetchAllTasks.as_view(), name='task-fetch'),
] 