ReST API
========

There will be built-in support for a ReST API allowing for connections in
mobile apps or in other use cases. In order to use the API, you first need to
get access to an API Key. At the moment, the only way to get an API key is to
add one manually in the config.

General Usage
-------------

API Token
^^^^^^^^^

All API requests will have to supply the API key somewhere in the request:

    For GET Requests, add the :code:`key` GET parameter.

    .. code-block:: bash

        /api/apiStuff?key='your-api-key'
    
    For POST Requests, add the :code:`key` header

Errors
^^^^^^

All requests will return either success, or failure. On failure, a return code
will be given, as well as context for more information.

The return code is used to let the program know what happened, and the context
is used to let the user know what happened.

.. code-block:: typescript

    interface Error {
        message: string
    }

Weather API
-----------

Current Weather
^^^^^^^^^^^^^^^

.. function:: /api/weather/now

    :type: GET

    Get the current weather

    :return:

        A json object containing the latest weather data

        .. code-block:: typescript

            interface DataPoint {
                time: DateTime,
                data: {
                    [key: string]: {
                        value: number,
                        type: string
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

        A Json Object containing all the datapoints for the request

        .. code-block:: typescript

            interface DataPoint {
                time: DateTime,
                data: {
                    [key: string]: {
                        value: number,
                        type: string
                    }
                }
            }

            interface HistoryResponse {
                history: Array<DataPoint>
            }

Settings
--------

Get
^^^

.. function:: /api/settings/get/<slug:app>

    :type: GET
    :permissions: Settings

    Get a the settings for an app

    :param app: The name of the app

    :return: Settings

        .. code-block:: typescript

            interface SetResponse {
                [key: string]: string | number | Array<string> | boolean
            }

Set
^^^

.. function:: /api/settings/set/<slug:app>

    :type: POST
    :permissions: Settings

    Change an app's settings

    :param app: The name of the app

    :body: Settings to apply

        .. code-block:: typescript

            interface SetBody {
                [key: string]: string | number | Array<string> | boolean
            }
    
    :return: Settings

        .. code-block:: typescript

            interface SetResponse {
                [key: string]: string | number | Array<string> | boolean
            }

Apply
^^^^^

.. function:: /api/settings/apply

    :type: GET
    :permissions: Settings

    Apply the changed settings to disk. 

Load
^^^^

.. function:: /api/settings/load

    :type: GET
    :permissions: Settings

    Load the settings from what's stored on disk
