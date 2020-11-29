from django.conf.urls import url, include
from django.urls import path
from . import views


app_name = 'dectree'

urlpatterns = [
    url(r'^$', views.dectree_index, name='dectree_index'),
    url(r'^upload/', views.upload_form, name='dectree_upload'),
    url(r'^results/', views.show_results, name='dectree_results')
]

