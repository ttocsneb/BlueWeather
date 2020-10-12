from django.urls import path

from . import views


urlpatterns = [
    path("interfaces", views.get_settings_interfaces, name="interfaces"),
    path("get/<slug:app>", views.get_settings, name="get"),
    path("set/<slug:app>", views.set_settings, name="set"),
    path("revert", views.revert_settings, name="revert"),
    path("apply", views.apply_settings, name="apply")
]
