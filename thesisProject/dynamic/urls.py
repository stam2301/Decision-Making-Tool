from django.conf.urls import url, include
from django.urls import path, re_path
from . import views

app_name = 'dynamic'

urlpatterns = [
    url(r'^$', views.dynamic_index, name='dynamic_index'),
    url(r'^upload/', views.upload_form, name='dynamic_upload'),
    url(r'^create/', views.create_data, name='create_data'),
    path('results/<int:method_id>', views.results, name='results'),
    path('manage/<int:method_id>', views.manage, name='manage'),
    url(r'^ajax/calculate', views.ajax_calculate, name='ajax_calculate'),
    url(r'^ajax/create_and_calculate', views.ajax_create_and_calculate, name='ajax_create_and_calculate'),
    url(r'^ajax/upload_manage', views.ajax_upload_manage, name='ajax_upload_manage'),
    url(r'^ajax/upload_run', views.ajax_upload_run, name='ajax_upload_run')]