from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name
