# hack to import from sibling directory
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from django.conf.urls import url
import lists.views


urlpatterns = [
    url(regex=r'^new$', view=lists.views.new_list, name='new_list'),
    url(regex=r'^(\d+)/$', view=lists.views.view_list, name='view_list'),
    url(regex=r'^(\d+)/add_item$', view=lists.views.add_item, name='add_item')
]