from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        UnaccentExtension(),
        TrigramExtension(),
    ]
