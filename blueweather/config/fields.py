from marshmallow import fields, exceptions
import collections

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
    """

    def __init__(self, cls_or_instance, name_attr="name", value_attr="value",
                 remove_attr=True, value_only=False, **kwargs):
        """
        Create a NamedList Field

        :param str name_attr: attribute name of the key
        :param str value_attr: attribute name of the value if no dict is
            provided
        :param bool remove_attr: should the name attribute be removed when
            serializing
        :param bool value_only: is the value the only other value in the object
        """
        super().__init__(cls_or_instance, **kwargs)
        self._name_attr = name_attr
        self._value_attr = value_attr
        self._remove_attr = remove_attr
        self._value_only = value_only

    def _serialize(self, values, attr, obj, **kwargs):
        serialized = super()._serialize(values, attr, obj, **kwargs)
        obj = list()
        for value in serialized:
            name = value[self._name_attr]
            if self._remove_attr:
                del value[self._name_attr]

            if self._value_only:
                value = value[self._value_attr]
            elif len(value) == 1:
                try:
                    value = value[self._value_attr]
                except KeyError:
                    pass
            if not value:
                obj.append(name)
            else:
                obj.append({name: value})

        return obj

    def _deserialize(self, value, attr, data, **kwargs):
        deserialized = list()

        def parse_dict(k: str, v):
            if not isinstance(value, collections.Mapping):
                v = {self._value_attr: v}
            v[self._name_attr] = k
            deserialized.append(v)

        if isinstance(value, collections.Mapping):
            for k, v in value.items():
                parse_dict(k, v)
        else:
            for d in value:
                if isinstance(d, collections.Mapping):
                    # There should only be one key in this dict
                    k = list(d.keys())[0]
                    v = d[k]
                    parse_dict(k, v)
                else:
                    deserialized.append({
                        self._name_attr: d
                    })

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
