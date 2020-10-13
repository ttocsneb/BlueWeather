from django.apps.registry import apps
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import Widget
from django.urls import reverse
from django.utils import dateformat, datetime_safe, formats, timezone
from jinja2 import Environment

import json

from . import utils


def get_or_call(request, setting):
    if callable(setting):
        return setting(request)
    return setting


def parse_sidebar(obj: dict):
    item = dict(obj)

    def get_attr(var, attr, default=None):
        try:
            if hasattr(var, attr):
                return getattr(var, attr)
            return var[attr]
        except TypeError:
            pass
        except KeyError:
            pass
        return default

    def is_active_url(request, url):
        try:
            return str(request.path) == str(reverse(get_or_call(request, url)))
        except Exception:
            return False

    def is_active(request):
        if is_active_url(request, item['path']):
            return True
        sidebar_items = get_or_call(
            request, get_attr(item['value'], 'sidebar_items')
        )
        if sidebar_items is not None:
            for i in sidebar_items:
                if i["category"] != 'item':
                    continue
                if is_active_url(request, i['value']['route']):
                    return True

        return False

    if item['category'] == 'item':
        item['value'] = apps.get_app_config(item['value'])
        item['active'] = is_active
        item['path'] = get_attr(item['value'], 'route') \
            or get_attr(item['value'], 'name') + ':index'
        item['item'] = True
        item['login_required'] = get_attr(item['value'], 'login_required')
    else:
        item['item'] = False
    item['header'] = item['category'] == 'header'
    item['divider'] = item['category'] == 'divider'
    return item


sidebar = [parse_sidebar(x) for x in settings.SIDEBAR]


def now():
    tz = timezone.get_current_timezone() if settings.USE_TZ else None
    return datetime_safe.datetime.now(tz=tz)


def add_attrs(widget: Widget, attr, *args):
    """
    Add css classes to a widget

    :param widget: widget to add classes
    :param args: space separated classes
    """
    args = ' '.join(args).split(' ')
    attr_values = widget.field.widget.attrs.get(attr, '').split(' ')
    for arg in args:
        if arg not in attr_values:
            attr_values.append(arg)
    widget.field.widget.attrs.update({attr: ' '.join(attr_values)})
    return widget


def add_classes(widget, *args):
    """
    Add css classes to a widget

    :param widget: widget to add classes
    :param args: space separated classes
    """
    return add_attrs(widget, 'class', *args)


def set_attr(widget, attr, value):
    """
    Add values to an attr of a widget

    :param widget: widget to add to
    :param str atr: name of attribute
    :param value: value
    """
    widget.field.widget.attrs.update({attr: value})
    return widget


def to_json(data: dict) -> str:
    """
    Convert an object into a json string

    :param data: data to serialize

    :return: serialized json
    """
    return json.dumps(data, cls=utils.JsonEncoder)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'time': dateformat.format,
        'now': now,
        'number': formats.number_format,
        'sidebar': sidebar,
        'add_attrs': add_attrs,
        'set_attr': set_attr,
        'add_classes': add_classes,
        'get_or_call': get_or_call,
    })
    env.filters.update({
        'json': to_json
    })

    global_settings = {
        "LANGUAGE_CODE": "en",
        "DEFAULT_CHARSET": "utf-8",
        "DATE_FORMAT": "N j, Y",
        "DATETIME_FORMAT": "N j, Y, P",
        "FIRST_DAY_OF_WEEK": 0,
        "SHORT_DATE_FORMAT": "m/d/Y",
        "SHORT_DATETIME_FORMAT": "m/d/Y P",
        "TIME_FORMAT": "P",
        "YEAR_MONTH_FORMAT": "F Y",
        "DEBUG": False
    }

    env.globals.update(dict(
        [(s, getattr(settings, s, d)) for s, d in global_settings.items()]
    ))

    return env
