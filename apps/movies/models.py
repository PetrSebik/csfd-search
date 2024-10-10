from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=128)
    actors = models.ManyToManyField("Actor", related_name="movies")


class Actor(models.Model):
    name = models.CharField(max_length=128)


class Unaccent(models.Func):
    function = 'unaccent'
    template = '%(function)s(%(expressions)s)'
