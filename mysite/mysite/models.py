from django.db import models
from django.core.validators import MinValueValidator

from jmbo.models import ModelBase



class Manufacturer(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000)])

    def __unicode__(self):
        return self.title


class Car(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title
