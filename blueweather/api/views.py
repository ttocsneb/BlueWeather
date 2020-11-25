"""
Api Views
"""
from typing import Type, Optional, List
from marshmallow import Schema, ValidationError
import json
import inspect

from django.http.request import HttpRequest
from django.http.response import (
    HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse)
from django.utils.log import log_response
from django.urls import path

from .annotate import annotator
from . import parser


class Api:
    """
    Api Handler

    :param func: api function
    :param method: allowed request method types
    :param allow_get_params: whether to allow GET parameters when the method
        is not GET
    :param schema: result schema
    :param args_schema: request schema
    """
    def __init__(self, **kwargs):
        self.func: callable = kwargs.pop('func')
        self.sig = inspect.signature(self.func)
        self.methods: Optional[List[str]] = kwargs.pop('method', None)
        self.allow_get_params: bool = kwargs.pop('allow_get_params', True)
        self.args_schema: Type[Schema] = kwargs.pop('args_schema', None)
        self.schema: Optional[Type[Schema]] = kwargs.pop('schema', None)
        self._name: Optional[str] = kwargs.pop('name', None)

        if self.args_schema is None:
            self.args_schema = annotator.annotate(
                self.func,
                ignore=["request"]
            )

    @property
    def name(self):
        """
        The name of the api view
        """
        if self._name:
            return self._name
        else:
            return self.func.__name__

    @property
    def urlpattern(self):
        """
        The urlpattern for this view
        """
        return path("%s/" % self.name, self)

    def _merge(self, source, destination):
        """
        Recursive merge from source to destination

        :param source: source
        :param destination: destination

        :return: destination
        """
        for k, v in source.items():
            if isinstance(v, dict):
                node = destination.setdefault(k, {})
                if not isinstance(node, dict):
                    node = destination[k] = {}
                self._merge(v, node)
            else:
                destination[k] = v

        return destination

    def __call__(self, request: HttpRequest):
        """
        The actual view of the api

        :param request: request
        """
        # Assert the correct method type
        if self.method is not None and request.method not in self.methods:
            response = HttpResponseNotAllowed(self.methods)
            log_response(
                'Method Not Allowed (%s): %s', request.method, request.path,
                response=response,
                request=request
            )
            return response

        # Get the GET params
        if (request.method != 'GET' and self.allow_get_params) \
                or request.method == 'GET':
            params = parser.parseQueryDict(request.GET)
        else:
            params = {}

        # Get the POST params
        if request.body:
            try:
                post = json.loads(request.body, encoding=request.encoding)
                params = self._merge(post, params)
            except json.JSONDecodeError as error:
                response = HttpResponseBadRequest(str(error))
                log_response(
                    'Invalid Json (%s): %s', str(error), request.path,
                    response=response,
                    request=request
                )
                return response

        # Parse the arguments
        args_schema = self.args_schema()
        try:
            args = args_schema.load(params)
            if 'request' in self.sig.parameters:
                args['request'] = request
            bound = self.sig.bind(**args)
        except (ValidationError, TypeError) as error:
            response = HttpResponseBadRequest(str(error))
            log_response(
                'Invalid Parameters (%s): %s', str(error), request.path,
                response=response,
                request=request
            )
            return response

        # Run the api
        result = self.func(*bound.args, **bound.kwargs)

        # Dump the results
        if self.schema is not None:
            schema = self.schema()
            result = schema.dump(result)

        return JsonResponse(result)
