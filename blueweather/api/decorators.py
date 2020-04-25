from django.http import HttpResponseForbidden
from django.http.request import HttpRequest
from django.conf import settings


def AuthorizationRequired(fn: callable, fail_view: callable = None
                          ) -> callable:
    """
    Require Authorization to access the view.
    Authorization will allow either a logged in user, or a valid api_key.
    This means that a user does not have to be logged in to access the view,
    but will always be given access if the user is logged in

    :TODO: add a parameter to require specific permissions of logged in users.

    Please note that csrf tokens are not used in the authentication

    If fail_view is not provided, a httpResponseForbidden exception will be
    raised

    :param view fn: The view that will be displayed if authorized
    :param view fail_view: The view that will be displayed if not authorized
    """
    def CheckAuthorization(request: HttpRequest):
        def authorize():
            if request.method == 'GET':
                api_key = request.GET.get('api_key')
            else:
                api_key = request.POST.get('api_key')
            if api_key == settings.CONFIG.web.api_key:
                return True
            if request.user.is_authenticated:
                return True
            return False

        if authorize():
            return fn(request)

        if fail_view is not None:
            return fail_view(request)
        raise HttpResponseForbidden()

    return CheckAuthorization
