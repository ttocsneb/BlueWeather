from django.http.request import HttpRequest

from django.shortcuts import render
from django.urls import Resolver404

from blueweather.accounts.methods import get_user_data


def badRequest(request: HttpRequest, exception=None):
    context = dict(
        error="Bad Request", code=400,
        message="I don't know what you are trying to do, but it didn't work"
    )

    return render(request, "error.html", context=context, status=400)


def forbidden(request: HttpRequest, exception=None):
    context = dict(
        error="Forbidden", code=403,
        message="You weren't supposed to do that."
    )

    return render(request, "error.html", context=context, status=403)


def internalServerError(request: HttpRequest, exception=None):
    context = dict(
        error="Internal Server Error", code=500,
        message="I'm sorry, I made a mistake."
    )

    return render(request, "error.html", context=context, status=403)


def pageNotFound(request: HttpRequest, exception: Resolver404 = None):
    context = dict(
        error="Page Not Found", code="404",
        message="It looks like you found a glitch in the matrix..."
    )

    if isinstance(exception, Resolver404):
        exception = exception.args[0]

    if isinstance(exception, dict):
        context['error'] = exception.get('path', '') + " Not Found"
    return render(
        request, "error.html", context=context, status=404
    )


def index(request: HttpRequest):
    return render(request, "base.html", context={
        'user_data': get_user_data(request.user)
    })
