from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='POST',
    operation_description='Create a new task',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['title', 'description'],
    ),
    responses={
        201: 'Task created successfully',
        400: 'Invalid data provided',
    }
)
@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(
    method='GET',
    operation_description='Retrieve all tasks',
    manual_parameters=[
        openapi.Parameter(
            name='status',
            in_=openapi.IN_QUERY,
            description='Status filter for tasks',
            required=False,
            type=openapi.TYPE_STRING,
            enum=['all', 'completed', 'incomplete'],
        ),
    ],
    responses={
        200: 'Tasks retrieved successfully',
    }
)
@api_view(['GET'])
def get_all_tasks(request):
    status = request.query_params.get('status')

    if status == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif status == 'incomplete':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET',
    operation_description='Retrieve a specific task',
    responses={
        200: 'Task details retrieved successfully',
        404: 'Task not found',
    }
)
@swagger_auto_schema(
    method='PATCH',
    operation_description='Update a specific task',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
        required=None,
    ),
    responses={
        200: 'Task updated successfully',
        400: 'Invalid data provided',
        404: 'Task not found',
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description='Delete a specific task',
    responses={
        204: 'Task deleted successfully',
        404: 'Task not found',
    }
)
@api_view(['GET', 'PATCH', 'DELETE'])
def task(request, task_id):
    if request.method == 'GET':
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=404)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=404)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=404)
        task.delete()
        return Response(status=204)
