from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index')
]


def get_api_urlpatterns():
    return [
        path("apply", views.set_settings, name="apply"),
        path("save", views.save_settings, name="save"),
        path("revert", views.save_settings, name="revert")
    ]
