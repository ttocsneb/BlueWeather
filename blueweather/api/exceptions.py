"""
Exceptions that can be raised in an api function
"""
import json
from django.http.response import JsonResponse


class APIError(Exception):
    """
    The base exception for all api exceptions
    """
    def __init__(self, code: int = 400, detail: str = "API Error", **kwargs):
        self.code = code
        self.detail = detail
        self.details = kwargs
        self.details.update({
            'code': code,
            'detail': detail
        })

    def response(self):
        return JsonResponse(self.details)

    def __str__(self):
        return json.dumps(self.details)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '{}={}'.format(k, repr(v))
                for k, v in self.details.items()
            )
        )
