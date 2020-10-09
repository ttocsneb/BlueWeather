from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index')
]


def get_api_urlpatterns():
    return [
        path("interface", views.get_settings_interface, name="interface"),
        path("settings", views.get_settings, name="settings"),
        path("revert", views.revert_settings, name="revert"),
        path("apply", views.apply_settings, name="apply")
    ]
