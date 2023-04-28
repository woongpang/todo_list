from django.contrib import admin
from .models import TodoList


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_complete",
        "created_at",
        "updated_at",
        "completion_at",
        "user",
    )