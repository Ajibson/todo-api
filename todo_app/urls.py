from django.urls import path
from .views import TodoListCreate, TodoRetrieveUpdateDestroy

urlpatterns = [
    path('', TodoListCreate.as_view(), name='todo-list-create'),
    path('<int:pk>', TodoRetrieveUpdateDestroy.as_view(), name='todo-retrieve-update-destroy'),
]
