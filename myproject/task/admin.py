from django.contrib import admin
from django import forms
from django.forms import widgets

# Register your models here.
from .models import Priority, Category, Task, Note, SubTask

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'deadline': forms.DateInput(
                attrs={'type': 'date', 'class': 'vDateField'}
            )
        }

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ("title", "status")
    show_change_link = True

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ("content", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ("title", "status", "deadline", "priority", "category")
    list_filter = ("status", "priority", "category", "deadline")
    search_fields = ("title",)
    date_hierarchy = 'deadline'

    inlines = [SubTaskInline, NoteInline]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "content", "created_at",)
    list_filter = ("created_at",)
    search_fields = ("content",)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "parent_task",)
    list_filter = ("status",)
    search_fields = ("title",)
    
