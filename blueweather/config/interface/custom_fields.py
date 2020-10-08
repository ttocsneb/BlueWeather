from marshmallow import fields, ValidationError

from typing import Tuple, Dict, Any


class Choice(fields.String):
    """
    The Union between any types.
    """
    def __init__(self, options: Tuple[str], case_sensitive: bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not case_sensitive:
            self._options = dict(
                (option.lower(), option)
                for option in options
            )
        else:
            self._options = dict(
                (option, option)
                for option in options
            )
        self._case_sensitive = case_sensitive

    def _deserialize(self, value, attr, data, **kwargs):
        val = super()._deserialize(value, attr, data, **kwargs)
        if not self._case_sensitive:
            val = val.lower()
        try:
            return self._options[val]
        except KeyError as error:
            raise ValidationError('Not a valid option') from error


class Typed(fields.Field):
    """
    A field whose type changes depending on another field
    """
    def __init__(self, type: str, types: Dict[Any, fields.Field],
                 default_type: fields.Field = None,
                 type_field: fields.Field = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = type
        self._types = types
        self._default_type = default_type
        self._type_field = type_field or fields.Raw()
        if callable(self._type_field):
            self._type_field = self._type_field()

    def _serialize(self, value, attr, obj, **kwargs):
        declared_type = self.get_value(obj, self._type)
        return self._types.get(declared_type, self._default_type)._serialize(
            value, attr, obj, **kwargs
        )

    def _deserialize(self, value, attr, data, **kwargs):
        raw_type = self.get_value(data, self._type)
        declared_type = self._type_field.deserialize(
            raw_type, self._type, data, **kwargs
        )
        if self._default_type is None and declared_type not in self._types:
            raise ValidationError('invalid type parameter')
        return self._types.get(declared_type, self._default_type)._deserialize(
            value, attr, data, **kwargs
        )
