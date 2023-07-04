from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


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


@api_view(['GET', 'PUT', 'DELETE'])
def task(request, task_id):

    if request.method == 'GET':
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=404)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=404)
        serializer = TaskSerializer(task, data=request.data)
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