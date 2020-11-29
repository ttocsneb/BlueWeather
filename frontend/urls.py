from django.urls import path

from . import views


handler404 = 'frontend.views.pageNotFound'
handler403 = 'frontend.views.forbidden'
handler400 = 'frontend.views.badRequest'
handler500 = 'frontend.views.internalServerError'

urlpatterns = [
    path('', views.index)
]
