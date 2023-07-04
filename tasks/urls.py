from django.urls import path
from .views import create_task, get_all_tasks, get_task, update_task, delete_task

urlpatterns = [
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', get_task, name='get_task'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
]