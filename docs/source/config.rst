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

Secret Key
----------

.. attribute:: secret_key

    :type: str

    The secret key used by django. This is auto-generated and should not be shared
    with anyone.

Debug
-----

.. attribute:: debug

    :type: bool
    :default: false

    Should the server start in debug mode

    .. note::

        This should be set to false in almost all circumstances.

Time Zone
---------

.. attribute:: time_zone

    :type: str

    The time zone that your server is located in.

Commands
--------

.. attribute:: commands

    :type: dict

    A list of system commands that can control the server

    .. code-block:: python

        {
            'restart': 'command to restart the server',
            'shutdown': 'command to shutdown the computer',
            'stop': 'command to stop the server'
        }

Web
---

Static URL
^^^^^^^^^^

.. attribute:: web.static_url

    :type: str
    :default: `static`

    the endpoint of the static url.

Databases
^^^^^^^^^

.. attribute:: web.databases

    All the databases. I'm not entirely sure why I would need multiple databases,
    but the support is there.

    .. todo::
    
        Figure out what's going on.

Password Validation
^^^^^^^^^^^^^^^^^^^

.. attribute:: web.password_validation

    :type: list

    A list of django password validators used to validate passwords.

    :default:

        .. code-block:: python

            [
                "userAttributeSimilarityValidator",
                "MinimumLengthValidator",
                "CommonPasswordValidator",
                "NumericPasswordValidator"
            ]

Allowed Hosts
^^^^^^^^^^^^^

.. attribute:: web.allowed_hosts

    :type: list

    A list of hosts that the server will listen on.

Template Globals
^^^^^^^^^^^^^^^^

.. attribute:: web.template_globals

    :type: dict

    Global variables to be inserted into templates.

Sidebar
^^^^^^^

.. attribute:: web.sidebar

    The structure of the sidebar.

    .. todo::
    
        Add more info

Api Keys
^^^^^^^^

.. attribute:: web.api_keys

    :type: list

    A list of API keys and their permissions

    .. code-block:: python

        [
            {
                'key': 'key-value',
                'name': 'name of the key',
                'permissions': [
                    'permission'
                ]
            }
        ]

Extensions
----------

Weather Driver
^^^^^^^^^^^^^^

.. attribute:: extensions.weather_driver

    :type: str
    :default: `dummyWeather`

    The driver to use to get the weather.

Disabled
^^^^^^^^

.. attribute:: extensions.disabled

    :type: list

    A list of disabled plugins

Settings
^^^^^^^^

.. attribute:: extensions.settings

    :type: dict

    The settings for each plugin.