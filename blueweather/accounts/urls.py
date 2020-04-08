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
             template_name="accounts/logout.html"
         ), name="logout"),
    path("password_change/",
         auth_views.PasswordChangeView.as_view(
             template_name="accounts/password_change.html"
         ), name="password_change"),
    path("password_change/done/",
         auth_views.PasswordChangeDoneView.as_view(),
         name="password_change/done"),
    path("password_reset/",
         auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password_reset/done",
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("login/",
         auth_views.LoginView.as_view(),
         name="login"),
    path("profile/", views.profile, name="profile"),
]
