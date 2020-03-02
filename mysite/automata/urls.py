from django.urls import path

from . import views, textIn

urlpatterns = [
    path('input/', views.input, name='input'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('result/', views.result, name="result"),
]
