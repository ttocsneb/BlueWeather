Internal Docs
#############

Apps
====

The apps module contains all the django apps for BlueWeather.

Accounts App
------------

API App
-------

Plugins App
-----------

Weather App
-----------

Plugins
=======

The plugins module is the main module that manages :ref:`plugins`

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

Hooks
-----