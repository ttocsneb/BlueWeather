from django.apps.registry import apps
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils import dateformat, datetime_safe, formats, timezone
from jinja2 import Environment


def parse_sidebar(item: dict):
    if item['category'] == 'item':
        item['value'] = apps.get_app_config(item['value'])
    return item


sidebar = [parse_sidebar(x) for x in settings.SIDEBAR]


def now():
    tz = timezone.get_current_timezone() if settings.USE_TZ else None
    return datetime_safe.datetime.now(tz=tz)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'time': dateformat.format,
        'now': now,
        'number': formats.number_format,
        'sidebar': sidebar
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

    env.globals.update(settings.CONFIG.web.template_globals)

    return env
