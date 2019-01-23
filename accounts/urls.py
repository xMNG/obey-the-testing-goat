from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(regex=r'^send_email$', view=views.send_login_email, name='send_login_email'),
    url(regex=r'^login$', view=views.login, name='login'),
    url(regex=r'^logout$', view=views.logout, name='logout')
]
