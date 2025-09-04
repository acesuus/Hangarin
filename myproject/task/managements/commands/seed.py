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
            title = fake.sentence(nb_words=20)
            description = fake.paragraph(nb_sentences=5)
            status = fake.random_element(elements=status_choices)
            priority = random.choice(Priority.objects.all() if Priority.objects.exists() else None)
            category = random.choice(Category.objects.all()) if Category.objects.exists() else None

            Task.objects.create(
                title=title, 
                description=description,
                status=status,
                deadline = timezone.make_aware(fake.date_time_this_month),
                priority=priority,
                category=category
            )

        self.stdout.write(self.style.SUCCESS(
                    'Initial data for organization created successfully.'
                ))



    def create_notes(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())
        for _ in range(count):
            if not tasks:
                break
            task = random.choice(tasks)
            content = fake.paragraph(nb_sentences=5)
            Note.objects.create(
                task=task,
                content=content
            )
        self.stdout.write(self.style.SUCCESS(
            'Initial data for organization created successfully.'
        ))

    def create_subtask(self, count):
        fake = Faker()
        status_choices = [choice[0] for choice in SubTask.STATUS_CHOICES]
        tasks = list(Task.objects.all())
        for _ in range(count):
            if not tasks:
                break
            parent_task = random.choice(tasks)
            title = fake.sentence(nb_words=20)
            status = fake.random_element(elements=status_choices)
            SubTask.objects.create(
                parent_task=parent_task,
                title=title,
                status=status
            )
        self.stdout.write(self.style.SUCCESS(
            'Initial data for organization created successfully.'
        ))


