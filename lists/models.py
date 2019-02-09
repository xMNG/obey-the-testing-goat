from django.db import models
from django.conf import settings
from django.urls import reverse
from accounts.models import User
# Create your models here.


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    shared_with = models.ManyToManyField(to=User, related_name='shared_with_set')

    def get_absolute_url(self):
        """
        Gets absolute url of a list item
        :return: url string
        """
        return reverse(viewname='view_list', args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(to=List, default=None, on_delete=models.CASCADE, blank=False)  # blank=False means no blanks

    class Meta:
        unique_together = ('list', 'text')
        ordering = ('id',)

    def __str__(self):
        return self.text