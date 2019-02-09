import os
import sys

from django.conf.urls import url
import lists.views

# hack to import from sibling directory
sys.path.insert(0, os.path.abspath('..'))

urlpatterns = [
    url(regex=r'^new$', view=lists.views.new_list, name='new_list'),
    url(regex=r'^(\d+)/$', view=lists.views.view_list, name='view_list'),
    url(regex=r'^users/(.+)/', view=lists.views.my_lists, name='my_lists'),
    url(regex=r'^(\d+)/share/', view=lists.views.share_list, name='share_list')
]
