from django.conf.urls import url, include
from django.urls import path
from . import views


app_name = 'dectree'

urlpatterns = [
    url(r'^upload/', views.upload_form, name='dectree_upload')
]

