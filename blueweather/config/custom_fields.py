import collections
import re

from marshmallow import fields

from . import objects


def get_object(self, obj: objects.Config, **kwargs):
    self._obj = obj
    return obj


def strip_defaults(self, data, **kwargs):
    if not hasattr(self, "_obj") \
            or not hasattr(self._obj, "_defaults") \
            or not hasattr(self._obj, "_required"):
        return data
    new_data = dict()
    for k, v in data.items():
        if k in self._obj._required \
                or k not in self._obj._defaults \
                or v != self._obj._defaults[k]:
            new_data[k] = v
            continue
    return new_data


class ClassedList(fields.List):
    """
    A List Field that deserializes to a custom List Object
    """

    def __init__(self, cls, cls_or_instance, **kwargs):
        """
        Create A ClassedList Field

        :param cls: The class to deserialize to
        :param cls_or_instance: The type that the list contains
        """
        super().__init__(cls_or_instance, **kwargs)
        self._cls = cls

    def _deserialize(self, value, attr, data, **kwargs):
        lst = super()._deserialize(value, attr, data, **kwargs)
        return self._cls(lst)


class APIKey(fields.String):
    """
    A Uuid formatted string
    """

    def _format(self, value: str) -> str:
        return re.sub(r"[^0-9a-f]+", "", value.lower())

    def _deserialize(self, value, attr, data, **kwargs):
        uuid = super()._deserialize(value, attr, data, **kwargs)
        return self._format(uuid)

    def _serialize(self, value, attr, obj, **kwargs):
        uuid = self._format(value)
        chunk_size = 8
        chunks = [
            uuid[i:i + chunk_size] for i in range(0, len(uuid), chunk_size)
        ]
        return super()._serialize('-'.join(chunks), attr, obj, **kwargs)


class ClassString(fields.String):
    """
    Class String Name which can be prepended with a default module
    """

    def __init__(self, default_module=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_module = [i for i in default_module.split('.') if i]

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        modules = [i for i in value.split('.') if i]
        if len(modules) == 1:
            return '.'.join(self._default_module + modules)
        return '.'.join(modules)

    def _serialize(self, value, attr, obj, **kwargs):
        modules = value.split('.')
        if modules[:-1] == self._default_module:
            value = modules[-1]
        else:
            value = '.'.join(modules)
        return super()._serialize(value, attr, obj, **kwargs)


class NamedList(fields.List):
    """
    A data object that is serialized as a dictionary, and deserialized as a
    list of named objects

    The output of the serialized data will look something like this

    .. code-block:: json

        [
            {"key": {
                "val_key": "value",
                "other_data": "data"
            }}
            {"key": "value_only"},
            "key_only"
        ]

    This isn't very pretty, but looks very good in yaml

    .. code-block:: yaml

        list:
        - key:
            val_key: value
            other_data: data
        - key: value_only
        - key_only

    """

    def __init__(self, cls_or_instance, key_attr="name", value_attr="value",
                 **kwargs):
        """
        Create a NamedList Field

        :param cls_or_instance: The nested object
        :param key_attr: The attribute for the key
        :param value_attr: The attribute for the value

        """
        super().__init__(cls_or_instance, **kwargs)

        self._key_attr = key_attr
        self._val_attr = value_attr

    def _serialize(self, values: list, attr, obj, **kwargs):
        serialized = super()._serialize(values, attr, obj, **kwargs)
        if serialized is None:
            return None
        output = list()
        # Conver the serialized list into a named list
        for obj in serialized:
            # Get the key
            key = obj[self._key_attr]
            del obj[self._key_attr]
            # If the object only contains the key, then add the item as a
            # string
            if not obj:
                output.append(key)
                continue
            val = obj[self._val_attr]
            if len(obj) == 1 and not isinstance(val, dict):
                # If the value is the only other value, and it is not a dict
                output.append({key: val})
                continue
            output.append({key: obj})
        return output

    def _deserialize(self, value: list, attr, data, **kwargs):
        deserialized = list()

        for obj in value:
            if isinstance(obj, dict):
                # Parse the key -> data
                key, value = next(iter(obj.items()))
                if isinstance(value, dict):
                    value[self._key_attr] = key
                    deserialized.append(value)
                else:
                    deserialized.append({
                        self._key_attr: key,
                        self._val_attr: value
                    })
            else:
                # The obj is only the key
                deserialized.append({self._key_attr: obj})
        return super()._deserialize(deserialized, attr, data, **kwargs)


class Database(fields.Dict):
    """
    Database Setting field that deserializes to objects.Database
    """

    def __init__(self, **kwargs):
        super().__init__(keys=fields.String(), values=fields.String(),
                         **kwargs)

    def _serialize(self, value, attr, obj: objects.Database, **kwargs):
        value = get_object(self, value, **kwargs)

        value = super()._serialize(value, attr, obj, **kwargs)

        new_data = dict()
        for k, v in value.items():
            new_data[k.lower()] = v

        if new_data['engine'].startswith("django.db.backends."):
            new_data['engine'] = new_data['engine'].split('.')[-1]
        return strip_defaults(self, new_data, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        obj = super()._deserialize(value, attr, data, **kwargs)

        if '.' not in obj['engine']:
            obj['engine'] = 'django.db.backends.' + obj['engine']

        return objects.Database(**obj)
