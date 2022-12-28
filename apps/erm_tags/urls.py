from django.contrib import admin
from django.urls import path, include

from apps.erm_tags import views


urls = [
    path('', views.ErmInventoryView.as_view(), name='erm-inventory'),
]
