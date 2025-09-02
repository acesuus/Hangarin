from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Priority(BaseModel):
    name = models.CharField(max_length=250)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} (Level {self.level})"

class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):    
        return self.name

class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=100 )
    description = models.CharField(max_length=250, null=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="Pending")
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    category = models.ForeignKey(Category, null=True, blank=True, related_name="tasks")

    def __str__(self):
        return self.title
    
class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='note')
    content = models.TextField()
    def __str__(self):
        return self.task.title

class SubTask(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]


    parent_task = models.ForeignKey(Task, models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending" )
    
    def __str__(self):
        return f"{self.title} ({self.status})"
