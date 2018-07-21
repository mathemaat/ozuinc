from django.urls import path

from . import views

app_name = 'incassogen'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
]
