from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.shortcuts import render


@login_required
def index(request: HttpRequest):
    """
    The main page for the settings
    """
    return render(request, 'settings/settings.html', context={
        'name': 'Settings'
    })