from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page1', views.index1, name='index'),
    path('apply_Model', views.index2, name='index'),
]