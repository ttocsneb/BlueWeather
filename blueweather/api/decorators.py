from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from functools import wraps


def _authorize(request: HttpRequest, permissions: list):
    key = False
    auth = False
    if isinstance(permissions, str):
        permissions = [permissions]
    if permissions is None:
        permissions = []
    api_key = request.POST.get('api_key')
    if not api_key:
        api_key = request.GET.get('api_key')
    if api_key:
        api = settings.CONFIG.web.api_keys.get(api_key)
        if api is not None and \
                all(map(lambda i: i in api.permissions, permissions)):
            key = True
    if request.user.is_authenticated:
        auth = True
    return key, auth


def authorization_required(fn: callable, fail_view: callable = None,
                           permissions: list = None) -> callable:
    """
    Require Authorization to access the view.
    Authorization will allow either a logged in user, or a valid api_key.
    This means that a user does not have to be logged in to access the view,
    but will always be given access if the user is logged in

    :TODO: add a parameter to require specific permissions of logged in users.

    Please note that csrf tokens are not used in the authentication, and if you
    want csrf authorization, use csrf_authorization_required instead

    If fail_view is not provided, a httpResponseForbidden exception will be
    raised

    :param view fn: The view that will be displayed if authorized
    :param view fail_view: The view that will be displayed if not authorized
    """
    def CheckAuthorization(request: HttpRequest):
        if any(_authorize(request, permissions)):
            return fn(request)

        if fail_view is not None:
            return fail_view(request)
        raise PermissionDenied

    return wraps(fn)(CheckAuthorization)


def csrf_authorization_required(fn: callable, fail_view: callable = None,
                                permissions: list = None) -> callable:
    """
    Require Authorization to access the view.
    Authorization will allow either a logged in user, or a valid api_key.
    This means that a user does not have to be logged in to access the view,
    but will always be given access if the user is logged in

    If the user is logged in, and a token is provided, the csrf token does NOT
    get verified. otherwise, when a user is logged in, the csrf token will be
    verified.

    :TODO: add a parameter to require specific permissions of logged in users.

    If fail_view is not provided, a httpResponseForbidden exception will be
    raised

    :param view fn: The view that will be displayed if authorized
    :param view fail_view: The view that will be displayed if not authorized
    :param list/str permissions: A list of permissions that the key must have
    """
    def CheckAuthorization(request: HttpRequest):
        key, auth = _authorize(request, permissions)
        print("key, auth %s %s" % (key, auth))
        # Pass the view if a valid key was provided
        if key:
            return requires_csrf_token(fn)(request)
        # Protect the view from csrf if only logged in
        if auth:
            return csrf_protect(fn)(request)
        # Fail the authorization
        if fail_view is not None:
            return fail_view(request)
        raise PermissionDenied
    CheckAuthorization.csrf_exempt = True

    return wraps(fn)(CheckAuthorization)
