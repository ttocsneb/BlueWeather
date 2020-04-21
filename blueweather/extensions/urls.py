from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='extensions'),
    path("plugins", views.plugin_list, name='plugin_list')
]
