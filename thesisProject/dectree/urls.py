from django.conf.urls import url, include
from django.urls import path, re_path
from . import views


app_name = 'dectree'

urlpatterns = [
    url(r'^$', views.dectree_index, name='dectree_index'),
    url(r'^upload/', views.upload_form, name='dectree_upload'),
    path('results/<int:method_id>', views.results, name='results'),
    url(r'^manage/', views.manage_tree, name='manage_tree')
]

