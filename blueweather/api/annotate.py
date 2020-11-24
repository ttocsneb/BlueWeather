"""
Annotate functions into Marshmallow Schemas
"""
import inspect

import collections.abc
from marshmallow import Schema, fields, post_load

from typing import Type


class String(fields.String):
    def __init__(self, output: type, *args, **kwargs):
        self._output = output
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        return self._output(super()._deserialize(value, attr, data, **kwargs))


class Bytes(fields.Raw):
    def __init__(self, output: type, *args, **kwargs):
        self._output = output
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        return self._output(super()._deserialize(value, attr, data, **kwargs))


class Sequence(fields.List):
    def __init__(self, output: type, *args, **kwargs):
        self._output = output
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        return self._output(super()._deserialize(value, attr, data, **kwargs))


class Set(fields.List):
    def __init__(self, output: type, *args, **kwargs):
        self._output = output
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        return self._output(super()._deserialize(value, attr, data, **kwargs))


class Mapping(fields.Dict):
    def __init__(self, output: type, *args, **kwargs):
        self._output = output
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        return self._output(super()._deserialize(value, attr, data, **kwargs))


class Annotator:
    annotations = [
        (inspect._empty, fields.Raw),
        (int, fields.Integer),
        (float, fields.Float),
        (bool, fields.Boolean),
        (str, String),
        (collections.ByteString, Bytes),
        (collections.Sequence, Sequence),
        (collections.Set, Set),
        (collections.Mapping, Mapping),
    ]

    def __init__(self):
        self._registered_schemas = {}
        self._building_schemas = set()

    def annotate_param(self, parameter: inspect.Parameter) -> fields.Field:
        """
        Annotate a field

        :param parameter: parameter

        :return: annotated field
        """
        params = {}
        if parameter.default == inspect._empty:
            params['required'] = True
        else:
            params['missing'] = parameter.default

        # Deal with Schemas inside Schemas
        if parameter.annotation in self._building_schemas:
            return fields.Nested(
                lambda: self._registered_schemas[parameter.annotation](),
                **params
            )

        # Simple types
        for t, f in self.annotations:
            if issubclass(parameter.annotation, t):
                return f(output=parameter.annotation, **params)

        # Advanced types
        try:
            return fields.Nested(
                self._registered_schemas[parameter.annotation],
                **params
            )
        except KeyError:
            # Create a new annotation
            return fields.Nested(
                self.annotate(parameter.annotation, True),
                **params
            )

    def annotate(self, func: callable, call_on_load=False) -> Type[Schema]:
        """
        Annotate the function into a schema

        :param func: function to annotate
        :param call_on_load: whether the schema should call the function when
            it is loaded

        :return: schema for the function
        """
        if call_on_load:
            if func in self._registered_schemas:
                return self._registered_schemas[func]
            self._building_schemas.add(func)
        sig = inspect.signature(func)
        params = {}
        for param in sig.parameters.values():
            params[param.name] = self.annotate_param(param)

        schema = Schema.from_dict(params, name=func.__name__)

        if call_on_load:
            def build_object(self, item, many, **kwargs):
                bound = sig.bind(**item)
                return func(*bound.args, **bound.kwargs)
            schema.build_object = post_load(build_object)
            # TODO: This doesn't register the build_object as a post_load
            # function
            self._building_schemas.remove(func)
            self._registered_schemas[func] = schema

        return schema
