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

        self._weather = None
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
