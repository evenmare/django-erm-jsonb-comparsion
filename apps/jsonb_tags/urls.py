from django.contrib import admin
from django.urls import path, include

from apps.jsonb_tags import views


urls = [
    path('', views.JsonbInventoryView.as_view(), name='jsonb-inventory'),
]
