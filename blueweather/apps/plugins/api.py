from django.urls import path

from . import views


urlpatterns = [
    path("list", views.plugin_list, name='plugin_list')
]
