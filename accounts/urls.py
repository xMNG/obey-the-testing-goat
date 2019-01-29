import os
import sys

from django.conf.urls import url
from django.contrib.auth.views import logout
import accounts.views

# hack to import from sibling directory
sys.path.insert(0, os.path.abspath('..'))

urlpatterns = [
    url(regex=r'^send_login_email$', view=accounts.views.send_login_email, name='send_login_email'),
    url(regex=r'^login$', view=accounts.views.login, name='login'),
    url(regex=r'^logout$', view=logout, kwargs={'next_page': '/'}, name='logout')
]
