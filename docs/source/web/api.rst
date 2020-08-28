ReST API
========

There will be built-in support for a ReST API allowing for connections in
mobile apps or in other use cases. In order to use the API, you first need to
get access to an API Key. At the moment, the only way to get an API key is to
add one manually in the config.

All API requests will have to supply the API key somewhere in the request:

    For GET Requests, add the :code:`key` GET parameter.

    .. code-block:: bash

        /api/apiStuff?key='your-api-key'
    
    For POST Requests, add the :code:`key` header

Weather API
-----------

Current Weather
^^^^^^^^^^^^^^^

.. function:: /api/weather/now

    :type: GET

    Get the current weather

    :return:

        A json object containing all the weather data

        .. code-block:: json

            {
                "time": "The time when the data was recorded",
                "data": {
                    "tempurature": {
                        "value": 27.4,
                        "type": "c"
                    }
                }
            }

Weather history
^^^^^^^^^^^^^^^

.. function:: /api/weather/history(date: str, days: int, hours: int, minutes: int)

    :type: GET

    Retreive a set of data from a day during a time period.

    :param date: The date to start retreiving weather

        If omitted, the current day will be used.

    :param days: The number of days to look for data
    :param hours: The number of hours to look for data
    :param minutes: The number of minutes to look for data

    The default time frame will be 1 day if no time frame is given

    Examples:

        Get the history of the current day

        .. code-block:: bash

            /api/weather/history

        Get the history of the day `August 28, 2020`

        .. code-block:: bash

            /api/weather/history?date='2020-8-28'

        Get the history of the past two days

        .. code-block:: bash

            /api/weather/history?days=2

        Get the history of the day `August 28, 2020` and the day before

        .. code-block:: bash

            /api/weather/history?date='2020-8-28'&days=2

    :return:
        A list of weather data objects

        .. code-block:: json

            [
                {
                    "time": "The time when the data was recorded",
                    "data": {
                        "tempurature": {
                            "value": 27.4,
                            "type": "c"
                        }
                    }
                }
            ]

Settings
--------

Get
^^^

.. function:: /api/settings/get(group: str)

    :type: GET
    :permissions: Settings

    Get a list of the settings

    :param group: The optional groupname. If no group is given, all groups are returned

    :return: The settings

Change
^^^^^^

.. function:: /api/settings/change(settings: object)

    :type: POST
    :permissions: Settings

    Change a setting's value

    :param settings: An object of key-value pair setings

        .. code-block:: json

            {
                "group:setting-name": "Whatever-Settings-Object Required"
            }
