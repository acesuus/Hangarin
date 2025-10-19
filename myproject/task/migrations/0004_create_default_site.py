from django.db import migrations
from django.conf import settings

def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    # Delete any existing sites first
    Site.objects.all().delete()
    # Create new default site
    Site.objects.create(
        id=1,
        domain='127.0.0.1:8000',
        name='Hangarin Development'
    )

def remove_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(id=settings.SITE_ID).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('task', '0003_alter_task_description'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_default_site, remove_default_site),
    ]