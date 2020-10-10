.. currentmodule:: blueweather.plugins.base

.. _plugins:

API Reference
-------------

.. autosummary::

    App
    Weather
    UnitConversion
    blueweather.plugins.hooks.get_hook
    blueweather.plugins.hooks.Hook

.. automodule:: blueweather.plugins.base
    :members:

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