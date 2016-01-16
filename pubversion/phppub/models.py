from django.db import models

# Create your models here.

class Phpversion(models.Model):
    version = models.CharField(max_length=20)

    def __unicode__(self):
        return self.version


class Phpproject(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    version = models.ManyToManyField(Phpversion)

    def __unicode__(self):
        return self.name

