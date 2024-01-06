from rest_framework.response import Response
from rest_framework import status
from account.utils import pack_response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone

class TodoListCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(pack_response(1, serializer.data), status.HTTP_201_CREATED)
    
    def get(self, request):
        queryset = Todo.objects.filter(user=request.user).order_by('-starred')
        serializer = TodoSerializer(queryset, many=True)
        return Response(pack_response(1, serializer.data))

class TodoRetrieveUpdateDestroy(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk = pk)
            serializer = TodoSerializer(todo)
            return Response(pack_response(1, serializer.data))
        except Todo.DoesNotExist:
            return Response(pack_response(0, "Todo does not exist"), status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        try:
            todo = Todo.objects.get(pk = pk)
            serializer = TodoSerializer(instance=todo, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(pack_response(1, serializer.data))
        except Todo.DoesNotExist:
            return Response(pack_response(0, "Todo does not exist"), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            if todo.to_be_deleted_at is None:
                todo.to_be_deleted_at = timezone.now() + timedelta(seconds=5)
                todo.save()
                return Response(pack_response(1, "Todo moved to bin"), status=status.HTTP_202_ACCEPTED)
            else:
                return Response(pack_response(0, "Todo already in bin"), status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response(pack_response(0, "Todo does not exist"), status.HTTP_400_BAD_REQUEST)