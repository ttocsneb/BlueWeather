from yapsy.IPlugin import IPlugin


class BlueWeatherPlugin(IPlugin):
    """
    The parent class of all BlueWeather plugin mixins

     .. atribute:: _weather

        The :class: `~blueweather.weather.WeatherInterface` instance.
                    Injected by the plugin core system upon initialization

    """

    def __init__(self):
        self.is_activated = False

        self._status = None
        self._logger = None

    def activate(self):
        """
        Called at plugin activation.
        """
        self.is_activated = True

    def deactivate(self):
        """
        Called when the plugin is disabled.
        """
        self.is_activated = False


class StartupPlugin(BlueWeatherPlugin):
    """
    The ``StartupPlugin`` allows hooking into the startup of BlueWeather.  It
    can be used to startup additional services on or just after the startup of
    the server.
    """

    def __init__(self):
        super(StartupPlugin, self).__init__()

    def on_startup(self, host, port):
        """
        Called just before the server is actually launched.  Plugins get
        supplied with the ``host`` and ``port`` the server will listen on.
        Note that the ``host`` may be ``0.0.0.0`` if it will listen on all
        interfaces.

        :param string host: the host the server will listen on, may be
        ``0.0.0.0``

        :param int port: the port the server will listen on
        """

        pass

    def on_after_startup(self):
        """
        Called after the the webserver has started running
        """

        pass


class RequestsPlugin(BlueWeatherPlugin):
    """
    The ``RequestsPlugin`` allows hooking into the requests of the website.
    """

    def __init__(self):
        super(RequestsPlugin, self).__init__()

    def before_request(self, path: str, args: dict):
        """
        Called just before the server serves the client

        ``http://blueweather.com/foo/bar?arg1=asdf&arg2=qwerty``

        :param str path: the path of the url: ``foo/bar``

        :param dict args: the url args: ``{'arg1': 'asdf', 'arg2': 'qwerty'}``
        """

        pass


class WeatherPlugin(BlueWeatherPlugin):
    """
    Contains all of the necessary hooks for a weatherstation
    """

    def __init__(self):
        super(WeatherPlugin, self).__init__()

    def on_status_request(self):
        """
        Called when the status should be updated.  You can update the status
        through ``self._status`` which is a
        :class:``~blueweather.weather.status.Status``
        """

        pass
