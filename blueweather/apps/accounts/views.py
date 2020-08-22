from django.shortcuts import render, redirect


def profile(request):
    return render(request, "accounts/profile.html", context={
        'name': 'Profile'
    })


def index(request):
    return redirect('profile', permanent=True)
