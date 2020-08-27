Config
======

The config is the main way of changing the behaviour of BlueWeather.

Example Config

.. code-block:: yaml

    commands: 
      restart: ''
      shutdown: ''
      stop: ''
    debug: true
    extensions:
      disabled: []
      settings:
        dummySettings: 
        _version: 1
        description: Yeet My Feet
      weather_driver: dummyWeather
    secret_key: fe#c_@_&%0v4gvv0pivtj+b*!aafttzlo6v7&6%9v^+7^dmgx0
    web:
      api_keys:
      - key: 42237522-c7027c31-f90f5e34-b513c5a6
        name: default
      databases:
        default: 
        engine: sqlite3
        path: db.sqlite3
      password_validation: 
        - UserAttributeSimilarityValidator
        - MinimumLengthValidator
        - CommonPasswordValidator
        - NumericPasswordValidator
      template_globals: 
      title: BlueWeather


Base Group
----------

.. _secret_key:

secret_key
^^^^^^^^^^

The secret key used by django. This is auto-generated and should not be shared
with anyone.

.. _debug:

debug
^^^^^

Should the server start in debug mode

    default: false

.. note::

    This should be set to false in almost all circumstances.

.. _time_zone:

time_zome
^^^^^^^^^

The time zone that your server is located in.

.. _commands:

commands
^^^^^^^^

A list of system commands that can control the server

.. code-block:: python

    [
        'restart': 'command to restart the server',
        'shutdown': 'command to shutdown the computer',
        'stop': 'command to stop the server'
    ]

.. _web:

web Group
---------

.. _static_url:

static_url
^^^^^^^^^^

the endpoint of the static url.

    default: `static`

.. _databases:

databases
^^^^^^^^^

All the databases. I'm not entirely sure why I would need multiple databases,
but the support is there.

.. _password_validation:

password_validation
^^^^^^^^^^^^^^^^^^^

A list of django password validators used to validate passwords.

default:

.. code-block:: python

    [
        "userAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator"
    ]

.. _allowed_hosts:

allowed_hosts
^^^^^^^^^^^^^

A list of hosts that the server will listen on.

.. _template_globals:

template_globals
^^^^^^^^^^^^^^^^

Global variables to be inserted into templates.

.. _sidebar:

sidebar
^^^^^^^

The structure of the sidebar.

TODO, add more info

.. _api_keys:

api_keys
^^^^^^^^

A list of API keys and their permissions

.. code-block:: python

    {
        'key': 'key-value',
        'name': 'name of the key',
        'permissions': [
            'permission'
        ]
    }

.. _extensions:

extensions Group
----------------

.. _weather_driver:

weather_driver
^^^^^^^^^^^^^^

The driver to use to get the weather.

    default: `dummyWeather`

.. _disabled:

disabled
^^^^^^^^

A list of disabled plugins

.. _settings_config:

settings
^^^^^^^^

The settings for each plugin.