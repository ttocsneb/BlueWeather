.. currentmodule:: blueweather.plugins.base

.. _plugins:

Plugins
====================

Plugins are included using `stevedore <https://docs.openstack.org/stevedore/latest/>`_
This means that any package installed with `setup.py` can be turned into a plugin.

Creating A Plugin
-----------------

To create a simple plugin, you first need two files:

* setup.py
* `plugin_name`/__init__.py

setup.py holds the instructions on what your plugin needs to work, as well as
where entrypoints live.

For our simple plugin we will use the following code

.. code-block:: python

    import os
    from setuptools import setup, find_packages

    setup(
        name="SimplePlugin",
        version='0.0.1',
        
        entry_points={
            'blueweather.plugins.plugin': [
                # The left side of the equals sign is the internal name of our
                # plugin, it can't contain spaces, and must be unique. It does
                # not have to be pretty.
                'simplePlugin = simplePlugin:SimplePlugin'
            ],
            'blueweather.plugins.startup': [
                # The right side of the equals sign is the location of the class.
                # The format is module.names:ClassName
                'simplePlugin = simplePlugin:SimplePlugin'
            ]
        }
    )


The most import part of defining your plugin is its entrypoints. In the `setup`
function, the parameter `entry_points` tells BlueWeather what type of plugins
you are creating, as well as where its code lives.

For this example, we have defined two extensions:

* blueweather.plugins.plugin
* blueweather.plugins.startup

The :class:`~Plugin` extension gives usefull
information about the plugin, and is required for all plugins. The 
:class:`~Startup` extension requests a message 
for when the server is up and running.

Next we will create the file `simplePlugin/__init__.py`

.. code-block:: python

    from blueweather.plugin import base

    class SimplePlugin(base.Plugin, base.Startup):

        def get_plugin_name(self):
            return "Simple Plugin"
        
        def get_plugin_description(self):
            return "This is a simple plugin that prints 'Everything works!' when the server starts up"
        
        def on_startup(self):
            print("Everything works!")

This is where the code for the plugin lives. We have defined two required
functions for the :class:`~Plugin` extension (:meth:`~Plugin.get_plugin_name`,
and :meth:`~Plugin.get_plugin_description`)
This simply gives information about our plugin to the user. Then from the :class:`~Startup`
extension, we implement :meth:`~Startup.on_startup` where we print to the console that everything
is working.

This is an exceedingly simple plugin, but it should be enough to get you started
in creating your own plugins.

API Reference
-------------

.. autosummary::

    Plugin
    Startup
    API
    Settings
    Weather
    UnitConversion
    blueweather.plugins.hooks.get_hook
    blueweather.plugins.hooks.Hook

.. _plugin:

Plugin
^^^^^^

.. autoclass:: Plugin
    :members:

.. _startup:

Startup
^^^^^^^

.. autoclass:: Startup
    :members:

.. _api:

API
^^^

.. autoclass:: API
    :members:

.. _settings:

Settings
^^^^^^^^

.. autoclass:: Settings
    :members:

.. _weather:

Weather
^^^^^^^

.. autoclass:: Weather
    :members:

.. _unitConversion:

UnitConversion
^^^^^^^^^^^^^^

.. autoclass:: UnitConversion
    :members:

.. _hooks:

Hooks
-----

Hooks are ways that plugins can interact with eachother. They should not be
confused with stevedore's hooks though.

A hook is a list of functions that can be called. At any point in time, anyone
can create or subscribe to a hook. When the hook is called, all subscribed
functions will be called.

.. _get_hook:

get_hook
^^^^^^^^

.. autofunction:: blueweather.plugins.hooks.get_hook

.. _hook:

Hook
^^^^

.. autoclass:: blueweather.plugins.hooks.Hook
    :members: