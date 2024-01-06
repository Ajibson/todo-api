from django.core.management.base import BaseCommand
from django.utils import timezone
from todo_app.models import Todo

class Command(BaseCommand):
    help = 'Deletes todos that have been in the bin for more than 2 hours'

    def handle(self, *args, **kwargs):
        expired_todos = Todo.objects.filter(to_be_deleted_at__lt=timezone.now())
        count = expired_todos.count()
        expired_todos.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} todos'))
