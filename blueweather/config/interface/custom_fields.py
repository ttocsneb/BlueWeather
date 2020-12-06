import collections.abc
from marshmallow import fields, ValidationError, utils

from typing import Tuple, Dict, Any, List, Union


class Combine(fields.Field):
    """
    Union of several nested fields that are determined by a key

    :param nested: a dictionary of nested schemas
    :param key: the key to determine the schema to use
    :param key_field: the field to use to deserialize the key

    .. code-block:: python

        data = [{
            'type': 'a',
            'val': 'qwer'
        },
        {
            'type': 'b',
            'second': 5
        }]

        Union({'a': A, 'b': B}, key='type', key_field=fields.String(), many=True)
    """

    default_error_messages = {
        'bad_key': 'invalid key: {key}.'
    }

    def __init__(self, nested: List[Tuple[Union[str, List[str]], fields.SchemaABC]], key: str, key_field: fields.Field = None, **kwargs):
        self.key = key
        self.key_field = key_field
        if self.key_field is None:
            self.key_field = fields.Raw()
        self.nested = [
            (k, fields.Nested(v))
            for k, v in nested
        ]
        super().__init__(**kwargs)

    def _find_key(self, key_value):
        def contains(keys):
            if isinstance(keys, str):
                return key_value == keys
            if isinstance(keys, collections.Sequence):
                return key_value in keys
            return key_value == keys

        try:
            return next(
                v
                for k, v in self.nested
                if contains(k)
            )
        except StopIteration as stop:
            raise self.make_error('bad_key', key=repr(key_value)) from stop

    def _serialize(self, nested_obj, attr, obj, **kwargs):
        if utils.is_collection(nested_obj):
            def serialize(i, v):
                try:
                    return self._serialize(v, i, nested_obj, **kwargs)
                except ValidationError as error:
                    raise ValidationError({
                        i: error.message
                    }) from error
            return [
                serialize(i, v)
                for i, v in enumerate(nested_obj)
            ]
        key_value = utils.get_value(nested_obj, self.key)
        nested = self._find_key(key_value)
        return nested._serialize(nested_obj, attr, obj, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if utils.is_collection(value):
            def deserialize(i, v):
                try:
                    return self._deserialize(v, i, data, **kwargs)
                except ValidationError as error:
                    raise ValidationError({
                        i: error.normalized_messages()
                    }) from error
            return [
                deserialize(i, v)
                for i, v in enumerate(value)
            ]
        try:
            key_value = self.key_field._deserialize(
                value[self.key],
                self.key, value, **kwargs)
        except ValidationError as error:
            raise ValidationError({
                self.key: error.normalized_messages()
            }) from error
        nested = self._find_key(key_value)
        return nested._deserialize(value, attr, data, **kwargs)
