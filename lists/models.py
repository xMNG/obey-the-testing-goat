from django.db import models
from django.urls import reverse
# Create your models here.


class List(models.Model):

    def get_absolute_url(self):
        """
        Gets absolute url of a list item
        :return: url string
        """
        return reverse(viewname='view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(to=List, default=None, on_delete=models.CASCADE, blank=False)  # blank=False means no blanks
    # what about null=True ?

    class Meta:
        unique_together = ('list', 'text')
        ordering = ('id',)

    def __str__(self):
        return self.text