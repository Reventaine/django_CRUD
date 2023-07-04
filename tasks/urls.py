from django.urls import path
from .views import create_task, get_all_tasks, task

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Tasks_Django",
      default_version='v1',
      description="API documentation for Tasks API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task, name='task'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
