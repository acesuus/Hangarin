from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from .forms import TaskForm
from .models import Priority, Category, Task, Note, SubTask


class HomePageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return {}
        context = super().get_context_data(**kwargs)
        context['task_count'] = Task.objects.filter(user=self.request.user).count()
        context['category_count'] = Category.objects.filter(user=self.request.user).count()
        context['note_count'] = Note.objects.filter(task__user=self.request.user).count()
        context['subtask_count'] = SubTask.objects.filter(parent_task__user=self.request.user).count()
        context['priority_count'] = Priority.objects.filter(user=self.request.user).count()
        return context


# Priority Views
class PriorityListView(ListView):
    model = Priority
    template_name = "priority_list.html"
    context_object_name = "priorities"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(level__icontains=query)
            )
        
        ordering = self.request.GET.get('order_by', 'level')
        if ordering == 'name':
            qs = qs.order_by('name')
        elif ordering == '-name':
            qs = qs.order_by('-name')
        elif ordering == 'level':
            qs = qs.order_by('level', 'name')
        elif ordering == '-level':
            qs = qs.order_by('-level', 'name')
        return qs


class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = "priority_confirm_delete.html"
    success_url = reverse_lazy("priority-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Priority deleted.")
        return super().delete(request, *args, **kwargs)


class PriorityUpdateView(SuccessMessageMixin, UpdateView):
    model = Priority
    fields = ["name", "level"]
    template_name = "priority_form.html"

    def get_success_url(self):
        return self.request.path  # Stay on the same page
    success_message = "Priority saved successfully."


class PriorityCreateView(SuccessMessageMixin, CreateView):
    model = Priority
    fields = ["name", "level"]
    template_name = "priority_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path  # Stay on the same create form
    success_message = "Priority saved successfully. You can create another one."



class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        
        # Order by name
        ordering = self.request.GET.get('order_by', 'name')
        if ordering == '-name':
            qs = qs.order_by('-name')
        else:
            qs = qs.order_by('name')
        return qs


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("category-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Category deleted.")
        return super().delete(request, *args, **kwargs)


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    fields = ["name"]
    template_name = "category_form.html"
    def get_success_url(self):
        return self.request.path  # Stay on the same page
    success_message = "Category saved successfully."


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ["name"]
    template_name = "category_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path  # Stay on the same create form
    success_message = "Category saved successfully. You can create another one."


# Task Views
from datetime import date

class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(status__icontains=query)
            )
        
        # Order by various fields
        ordering = self.request.GET.get('order_by', 'deadline')
        if ordering == 'title':
            qs = qs.order_by('title')
        elif ordering == '-title':
            qs = qs.order_by('-title')
        elif ordering == 'deadline':
            qs = qs.order_by('deadline', 'priority__level', 'title')
        elif ordering == '-deadline':
            qs = qs.order_by('-deadline', 'priority__level', 'title')
        elif ordering == 'status':
            qs = qs.order_by('status', 'deadline', 'title')
        elif ordering == '-status':
            qs = qs.order_by('-status', 'deadline', 'title')
        elif ordering == 'priority':
            qs = qs.order_by('priority__level', 'deadline', 'title')
        elif ordering == '-priority':
            qs = qs.order_by('-priority__level', 'deadline', 'title')
        return qs


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Task deleted.")
        return super().delete(request, *args, **kwargs)


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    def get_success_url(self):
        return self.request.path  # Stay on the same page
    success_message = "Task saved successfully."


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['priority'].queryset = Priority.objects.filter(user=self.request.user)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form

    def get_success_url(self):
        return self.request.path  # Stay on the same create form
    success_message = "Task saved successfully. You can create another one."


# Note Views
class NoteListView(ListView):
    model = Note
    template_name = "note_list.html"
    context_object_name = "notes"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().filter(task__user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(task__title__icontains=query)
            )
        
        # Order by task and created date
        ordering = self.request.GET.get('order_by', '-created_at')
        if ordering == 'task':
            qs = qs.order_by('task__title', '-created_at')
        elif ordering == '-task':
            qs = qs.order_by('-task__title', '-created_at')
        elif ordering == 'created_at':
            qs = qs.order_by('created_at')
        elif ordering == '-created_at':
            qs = qs.order_by('-created_at')
        return qs


class NoteDeleteView(DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"
    success_url = reverse_lazy("note-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Note deleted.")
        return super().delete(request, *args, **kwargs)


class NoteUpdateView(SuccessMessageMixin, UpdateView):
    model = Note
    fields = ["task", "content"]
    template_name = "note_form.html"
    def get_success_url(self):
        return self.request.path  # Stay on the same page
    success_message = "Note saved successfully."


class NoteCreateView(SuccessMessageMixin, CreateView):
    model = Note
    fields = ["task", "content"]
    template_name = "note_form.html"
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['task'].queryset = Task.objects.filter(user=self.request.user)
        return form

    def get_success_url(self):
        return self.request.path  # Stay on the same create form
    success_message = "Note saved successfully. You can create another one."


# SubTask Views
class SubTaskListView(ListView):
    model = SubTask
    template_name = "subtask_list.html"
    context_object_name = "subtasks"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().filter(parent_task__user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(status__icontains=query) |
                Q(parent_task__title__icontains=query)
            )
        
        # Order by parent task, status, and title
        ordering = self.request.GET.get('order_by', 'parent_task')
        if ordering == 'parent_task':
            qs = qs.order_by('parent_task__title', 'status', 'title')
        elif ordering == '-parent_task':
            qs = qs.order_by('-parent_task__title', 'status', 'title')
        elif ordering == 'status':
            qs = qs.order_by('status', 'parent_task__title', 'title')
        elif ordering == '-status':
            qs = qs.order_by('-status', 'parent_task__title', 'title')
        elif ordering == 'title':
            qs = qs.order_by('title', 'parent_task__title')
        elif ordering == '-title':
            qs = qs.order_by('-title', 'parent_task__title')
        return qs


class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "subtask_confirm_delete.html"
    success_url = reverse_lazy("subtask-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "SubTask deleted.")
        return super().delete(request, *args, **kwargs)


class SubTaskUpdateView(SuccessMessageMixin, UpdateView):
    model = SubTask
    fields = ["parent_task", "title", "status"]
    template_name = "subtask_form.html"
    def get_success_url(self):
        return self.request.path  # Stay on the same page
    success_message = "SubTask saved successfully."


class SubTaskCreateView(SuccessMessageMixin, CreateView):
    model = SubTask
    fields = ["parent_task", "title", "status"]
    template_name = "subtask_form.html"
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['parent_task'].queryset = Task.objects.filter(user=self.request.user)
        return form

    def get_success_url(self):
        return self.request.path  # Stay on the same create form
    success_message = "SubTask saved successfully. You can create another one."
