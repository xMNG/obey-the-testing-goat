# hack to import from sibling directory
import os
import sys

from django.conf.urls import url
import lists.views

sys.path.insert(0, os.path.abspath('..'))

urlpatterns = [
    url(regex=r'^new$', view=lists.views.new_list, name='new_list'),
    url(regex=r'^(\d+)/$', view=lists.views.view_list, name='view_list'),
    url(regex=r'^(\d+)/add_item$', view=lists.views.add_item, name='add_item')
]
