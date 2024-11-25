from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
      path('index/', views.index, name='app1-index'),
      path('calcules/',views.calcules, name='calcules')
]