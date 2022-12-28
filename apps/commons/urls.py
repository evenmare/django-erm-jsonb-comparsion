from django.contrib import admin
from django.urls import path, include

from apps.commons import views

urls = [
    path('', views.index),
]
