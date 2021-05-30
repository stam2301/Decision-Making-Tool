from django.conf.urls import url, include
from django.urls import path, re_path
from . import views


app_name = 'mainapp'

urlpatterns = [
     url(r'^$', views.mainapp_index, name='mainapp_index'),
]