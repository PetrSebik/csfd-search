from django.db import models
from apps.movies.utils import remove_accents


class Movie(models.Model):
    name = models.CharField(max_length=128)
    name_unaccented = models.CharField(max_length=128, db_index=True)
    actors = models.ManyToManyField("Actor", related_name="movies")

    def save(self, *args, **kwargs):
        self.name_unaccented = remove_accents(self.name)
        super().save(*args, **kwargs)


class Actor(models.Model):
    name = models.CharField(max_length=128)
    name_unaccented = models.CharField(max_length=128, db_index=True)

    def save(self, *args, **kwargs):
        self.name_unaccented = remove_accents(self.name)
        super().save(*args, **kwargs)
