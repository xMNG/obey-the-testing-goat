"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# hack to import from sibling directory
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from django.conf.urls import include, url
from django.contrib import admin

import lists.views
from lists import views as list_views
from lists import urls as list_urls


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(regex=r'^$', view=lists.views.home_page, name='home'),
    url(regex=r'^lists/', view=include(list_urls)),
]
