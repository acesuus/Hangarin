from django.core.management.base import BaseCommand
from django.utils import timezone
from task.models import Task, Category, Priority, SubTask, Note
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populating Fake Data'

    def handle(self, *args, **options):
        self.create_task(20)
        self.create_notes(20)
        self.create_subtask(20)

    def create_task(self, count):
        fake = Faker()
        status_choices = [choice[0] for choice in Task.STATUS_CHOICES]
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        for _ in range(count):
            title = fake.sentence(nb_words=6)
            description = fake.paragraph(nb_sentences=3)
            status = fake.random_element(elements=status_choices)
            deadline = fake.date_between(start_date='today', end_date='+60d')
            priority = random.choice(priorities) if priorities else None
            category = random.choice(categories) if categories else None

            Task.objects.create(
                title=title,
                description=description,
                status=status,
                deadline=deadline,
                priority=priority,
                category=category
            )

        self.stdout.write(self.style.SUCCESS(
            'Tasks created successfully.'
        ))

    def create_notes(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())
        if not tasks:
            self.stdout.write(self.style.WARNING('No tasks available for notes.'))
            return
        for _ in range(count):
            task = random.choice(tasks)
            content = fake.paragraph(nb_sentences=3)
            Note.objects.create(
                task=task,
                content=content
            )
        self.stdout.write(self.style.SUCCESS(
            'Notes created successfully.'
        ))

    def create_subtask(self, count):
        fake = Faker()
        status_choices = [choice[0] for choice in SubTask.STATUS_CHOICES]
        tasks = list(Task.objects.all())
        if not tasks:
            self.stdout.write(self.style.WARNING('No tasks available for subtasks.'))
            return
        for _ in range(count):
            parent_task = random.choice(tasks)
            title = fake.sentence(nb_words=6)
            status = fake.random_element(elements=status_choices)
            SubTask.objects.create(
                parent_task=parent_task,
                title=title,
                status=status
            )
        self.stdout.write(self.style.SUCCESS(
            'Subtasks created successfully.'
        ))


