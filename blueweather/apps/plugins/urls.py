from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
]


def get_api_urlpatterns():
    return [
        path("list", views.plugin_list, name='plugin_list')
    ]
