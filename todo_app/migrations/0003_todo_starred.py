# Generated by Django 4.2.9 on 2024-01-05 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo_app", "0002_alter_todo_to_be_deleted_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo", name="starred", field=models.BooleanField(default=False),
        ),
    ]