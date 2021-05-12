from django.conf.urls import url, include
from django.urls import path, re_path
from . import views


app_name = 'dectree'

urlpatterns = [
    url(r'^$', views.dectree_index, name='dectree_index'),
    url(r'^upload/', views.upload_form, name='dectree_upload'),
    path('results/<int:method_id>', views.results, name='results'),
    path('manage/<int:method_id>', views.manage, name='manage'),
    #url(r'^manage/', views.manage_tree, name='manage_tree'),
    url(r'^create/', views.create_tree, name='create_tree'),
    url(r'^ajax/calculate', views.ajax_calculate, name='ajax_calculate'),
    url(r'^ajax/create_and_calculate', views.ajax_create_and_calculate, name='ajax_create_and_calculate')]



