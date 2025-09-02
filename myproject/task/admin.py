from django.contrib import admin

# Register your models here.
from .models import Priority, Category, Task, Note, SubTask

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name")
    search_fields = ("name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name")
    search_fields = ("name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "deadline", "priority", "category")
    list_filter = ("status", "priority", "category")
    search_fields = ("title")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "content", "created_at")
    list_filter = ("created_at")
    search_fields = ("content")

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "parent_task")
    list_filter = ("status")
    search_fields = ("title")
    
