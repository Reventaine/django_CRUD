from django.urls import path
from .views import create_task, get_all_tasks, task

urlpatterns = [
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task, name='get_task'),
    path('tasks/<int:task_id>/update/', task, name='update_task'),
    path('tasks/<int:task_id>/delete/', task, name='delete_task'),
]