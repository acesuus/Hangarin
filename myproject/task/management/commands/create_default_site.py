from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates the default site'

    def handle(self, *args, **options):
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': '127.0.0.1:8000',
                'name': 'Hangarin Development'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created default site'))
        else:
            site.domain = '127.0.0.1:8000'
            site.name = 'Hangarin Development'
            site.save()
            self.stdout.write(self.style.SUCCESS('Successfully updated default site'))