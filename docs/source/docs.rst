Internal Docs
#############

Here, you'll find the internal documentation for BlueWeather. It is currently
a mess, but I do plan to clean it up a bit as time goes on (hopefully).

.. role:: python(code)
    :language: python

Apps
====

The apps module contains all the django apps for BlueWeather.

Accounts App
------------

Manages the Accounts Page using :code:`auth` middleware from django

API App
-------

Manages the routes for all API patterns

Plugins App
-----------

Manages the Plugins page

Weather App
-----------

Displays the Weather Page

Templates
=========

The template system uses jinja2 and there are several custom commands added
that you can use.

Static
------

Calling :python:`static()` will find the url on the server for that static file.

.. code-block:: python

    static('path/to/static_file')

Url
---

Calling :python:`url()` will find the url from the patterns name.

.. code-block:: python

    url('url:name')

Time
----

Format a datetime object using PHP date() style formatting

.. code-block:: python

    time(now(), "Y-m-d H:i:s")

Now
---

Get the current time as a datetime object

.. code-block:: python

    now()

Number
------

Format a number using localization Settings

.. code-block:: python

    number(1000)
    number(1000.15, 1)

SideBar
-------

Get the sidebar object

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

Plugins
=======

The plugins module is the main module that manages :ref:`plugins`

ExtensionSingleton
------------------

.. autoclass:: blueweather.plugins.ExtensionsSingleton
    :members:

DAO
---

The DAO is the link between BlueWeather and the plugins.

Plugin
^^^^^^

.. autoclass:: blueweather.plugins.dao.Plugin
    :members:

Startup
^^^^^^^

.. autoclass:: blueweather.plugins.dao.Startup
    :members:

API
^^^

.. autoclass:: blueweather.plugins.dao.API
    :members:

Settings
^^^^^^^^

.. autoclass:: blueweather.plugins.dao.Settings
    :members:

Weather
^^^^^^^

.. autoclass:: blueweather.plugins.dao.Weather
    :members:

UnitConversion
^^^^^^^^^^^^^^

.. autoclass:: blueweather.plugins.dao.UnitConversion
    :members: