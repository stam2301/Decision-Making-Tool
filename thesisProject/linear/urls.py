from django.conf.urls import url, include
from django.urls import path, re_path
from . import views

app_name = 'linear'

urlpatterns = [
    url(r'^$', views.linear_index, name='linear_index'),
    url(r'^upload/', views.upload_form, name='linear_upload'),
    url(r'^create/', views.create_data, name='create_data'),
    path('results/<int:method_id>', views.results, name='results'),
    url(r'^ajax/create_and_calculate', views.ajax_create_and_calculate, name='ajax_create_and_calculate'),
]