from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("login/",
         auth_views.LoginView.as_view(
             template_name="accounts/login.html"
         ), name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(
             template_name="accounts/done.html",
             extra_context={
                 'message_header': "You have been logged out!",
                 'message': "Thanks for spending some quality time today."
             }
         ), name="logout"),
    path("password_change/",
         auth_views.PasswordChangeView.as_view(
             template_name="accounts/password_change.html"
         ), name="password_change"),
    path("password_change/done/",
         auth_views.PasswordChangeDoneView.as_view(
             template_name="accounts/done.html",
             extra_context={
                 'message_header': "Password change complete",
                 'message': "Your password was changed."
             }
         ), name="password_change_done"),
    path("profile/", views.profile, name="profile"),
    path("", views.index),
]
