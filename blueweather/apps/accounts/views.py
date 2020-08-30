from django.shortcuts import render, redirect


def profile(request):
    """
    Render the user's profile

    :template: `accounts/profile.html`
    """
    return render(request, "accounts/profile.html", context={
        'name': 'Profile'
    })


def index(request):
    """
    Redirect to the profile view

    :redirect: :meth:`~blueweather.apps.accounts.views.profile`
    """
    return redirect('profile', permanent=True)
