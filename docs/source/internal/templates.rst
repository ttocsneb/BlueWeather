.. role:: python(code)
    :language: python

Templates
=========

The template system uses jinja2 and there are several custom commands added
that you can use.

You can find all the function definitions in `blueweather.jinja2`

Static
------

.. function:: static(static_file: str) -> str

    Find the url path for a static file.

    :param static_file: static file path

    :return: url path for the static file

Url
---

.. function:: url(pattern: str) -> str

    Get the url from a url pattern.

    :param pattern: url pattern

    :return: url

    :example:

        >>> url("api:simplePlugin:apiName")
        /api/simpleplugin/apiname

Time
----

.. function:: time(value, format_string: str) -> str

    Format a datetime object into a format_string

    :param value: datetime object
    :param format_string: 'PHP format string <https://www.php.net/manual/en/datetime.format.php>'_

    :return: formatted datetime string

    :example:

        >>> time(now(), "Y-m-d H:i:s")
        2020-08-30 12:00:32

Now
---

.. function:: now() -> datetime.datetime

    Get the current time as a datetime object

    :return: time

Number
------

.. function:: number(number: float) -> str

    Format a number using localization Settings

    :param number: the number to localize

    :return: localized number string

    :example:

        >>> number(1000)
        1,000

SideBar
-------

.. function:: sidebar() -> list

    Get the sidebar object

    :return: List of sidebar objects

        .. code-block:: python

            [
                {
                    'category': 'item',
                    'value': 'value?',
                    'active': True,
                    'path': 'path:to:page'
                    'login_required': False,
                    # Item Type
                    'item': True,
                    'header': False,
                    'divider': False
                },
                {
                    'item': False,
                    'header': True,
                    'divider': False
                },
                {
                    'item': False,
                    'header': False,
                    'divider': True
                }
            ]

Add_attrs
---------

.. autofunction:: blueweather.jinja2.add_attrs

Set_attr
--------

.. autofunction:: blueweather.jinja2.set_attr

Add_classes
-----------

.. autofunction:: blueweather.jinja2.add_classes

Get_or_call
-----------

.. autofunction:: blueweather.jinja2.get_or_call

