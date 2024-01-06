from django.utils import timezone
from todo_app.models import Todo


def delete_todos():
    expired_todos = Todo.objects.filter(to_be_deleted_at__lt=timezone.now())
    count = expired_todos.count()
    expired_todos.delete()
    print(f'{timezone.now()}: Successfully deleted {count} todos')