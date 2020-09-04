from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from functools import wraps

from typing import Union, List, Tuple

def _authorize(request: HttpRequest, permissions: Union[str,List[str]]) -> Tuple[bool, bool]:
    """
    Check the authorization of a request

    .. TODO::

        Check if the user has the correct permissions

    :param request: Request to check
    :param permissions: Required permissions to check against

    :return key: whether the key was authenticated
    :return auth: whether the user was authenticated
    """
    key = False
    auth = False
    # Convert permission to a list if it is a string
    if isinstance(permissions, str):
        permissions = [permissions]
    if permissions is None:
        permissions = []
    # Get the API key
    api_key = request.POST.get('api_key')
    if not api_key:
        api_key = request.GET.get('api_key')
    if api_key:
        # Assert that the api key is valid
        api = settings.CONFIG.web.api_keys.get(api_key)
        if api is not None and \
                all(map(lambda i: i in api.permissions, permissions)):
            key = True
    # Check if the user is authenticated
    # TODO: Check if the user has the correct permissions
    if request.user.is_authenticated:
        auth = True
    return key, auth


def authorization_required(fn: callable, fail_view: callable = None,
                           permissions: Union[str, List[str]] = None) -> callable:
    """
    Require Authorization to access the view.
    Authorization will allow either a logged in user, or a valid api_key.
    This means that a user does not have to be logged in to access the view,
    but will always be given access if the user is logged in

    .. note::

        Csrf tokens are not used in the authentication, and if you want csrf
        authorization, use :meth:`csrf_authorization_required` instead

    If fail_view is not provided, a httpResponseForbidden exception will be
    raised

    :param fn: The view that will be displayed if authorized
    :param fail_view: The view that will be displayed if not authorized
    :param permissions: A list of required permissions
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

    .. note::

        If a token is provided, the csrf token will not be verified. In all
        other cases, the csrf token will be verified.

    If fail_view is not provided, a httpResponseForbidden exception will be
    raised

    :param fn: The view that will be displayed if authorized
    :param fail_view: The view that will be displayed if not authorized
    :param permissions: A list of permissions that the key must have
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
