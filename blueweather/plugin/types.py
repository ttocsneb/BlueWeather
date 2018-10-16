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

        self._logger = None

        self._data_folder = ''

        self._bundled = False

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

    def on_after_startup(self):
        """
        Called after the the webserver has started running
        """

        pass

    def on_shutdown(self):
        """
        Called after the server has shutdown.
        """

        pass


class RequestsPlugin(BlueWeatherPlugin):
    """
    The ``RequestsPlugin`` allows hooking into the requests of the website.
    """

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
        super().__init__()

        self._status = None
        self._weather = None

    def on_status_request(self):
        """
        Called when the status should be updated.  You can update the status
        through ``self._status`` which is a
        :class:``~blueweather.weather.status.Status``
        """

        pass

    def on_weather_request(self):

        pass


class SettingsPlugin(BlueWeatherPlugin):

    config_version_key = "_config_version"

    def __init__(self):
        super().__init__()

        self._settings = None

    def get_settings_defaults(self) -> dict:
        """
        Gets the plugins default settings

        This should return a dictionary with the default settings for the
        plugin
        """

        return dict()

    def get_settings_preprocessors(self) -> (dict, dict):
        """
        Gets the plugin's preprocessors to use for preprocessing returned or
        set values before returning or setting them.

        The dictionaries will be a path to the settings (can have nested
        dictionaries) The value being a transmorm function that gets the value
        as a parameter and returns the transformed value.

        Example::

            >>> def transform_some_key_getter(value) -> type(value):
                    return value.upper()

            >>> def transform_some_key_setter(value) -> type(value):
                    return value.lower()

            >>> def get_settings_preprocessors(self):
                    return dict(some_key=transform_some_key_getter),
                        dict(some_key=transform_some_key_setter)

        :return: (dict, dict): a tuple of two dicts.  The first for the
        plugin's preprocessor getters, and the second for the setters
        """

        return dict(), dict()

    def get_settings_version(self) -> int:
        """
        Get the plugin's settings version

        This can be used for migrations of old setting structures
        """

        return None

    def on_settings_migrate(self, target, current):
        """
        Called when the current setting's version does not match the supplied
        version

        :param int target: The target version, same value as returned by
        ``get_settings_version()``

        :param int current: (may be None) the current version that is saved
        """

        pass

    def on_settings_initialized(self):
        "Called after the settings have been initialized"

        pass

    def on_settings_save(self, data):
        """
        Saves the settings for the plugin

        :param dict data: The settings dictionary to be saved for the plugin


        :returns dict: The settiongs that differed fromt he defaults
        """

        from blueweather.util import dict_merge

        # Get the current Settings saved on disk
        current = self._settings.get_all_data()
        if current is None:
            current = dict()

        # Merge the new settings with the old settings
        new_current = dict_merge(current, data)
        if self.config_version_key in new_current:
            del new_current[self.config_version_key]

        version = self.get_settings_version()

        to_persist = new_current
        if version is not None:
            to_persist[self.config_version_key] = version

        return to_persist

    def on_settings_load(self):
        """
        Loads the settings for the plugin.

        :returns dict: the current settings of the plugin.
        """

        import copy

        data = copy.deepcopy(self._settings.get_all_data())
        if self.config_version_key in data:
            del data[self.config_version_key]

        return data


class TemplatePlugin(BlueWeatherPlugin):

    def get_template_configs(self):
        """
        Allows configuration of the settings.  I will implement more templates
        later on, but for now, only settings templates will be allowed.

        The function should return a list of dictionaries with each template.

        The dictionary contains the following


        ``type``: <``settings``, ``weather``, ``status``, ``dashboard_page``,
        ``weather_page``>
        The template type.

        ``name``:
        The name of the component.  If nothing is set, the name of the plugin
        will be used instead.  Some types, such as the weather type, do not
        use the name

        ``template``:
        The name of the template file to use

        ``id``:
        the div id that contains the component.  The default is
        ``<type>_plugin_<plugin identifier>``.

        ``variables``: dict
        A dictionary of variables to pass to the template engine.  You should
        use lambdas for variables that might change

        ``scripts``: list
        A list of urls to scripts to include.  You should use the
        `flask.url_for('plugin_id.static', filename='script')` to retrieve
        scripts located in the static directory

        Example:

        ```
        import flask
        return [
            dict(type='settings', template='my_template.jinja2',
                 variables=dict(foo='bar', qwerty=lambda: foo())),
            dict(type='settings', template='my_template_2.jinja2',
                 name='Hello World!', id='hello_world_settings'),
            dict(type='weather', template='weather.jinja2',
                 scripts=[flask.url_for('plugin_id.static',
                                        filename='js/script.js')])
        ]
        ```
        """

        pass


class RoutePlugin(BlueWeatherPlugin):

    def get_bluprint(self):
        """
        You can register a flask blueprint here by returning the created
        blueprint.

        This blueprint can be used to add routes to the website.

        A route can be created with the following code

        ```
        import flask

        my_blueprint = flask.Blueprint('my_blueprint', __name__)

        @my_blueprint.route('/plugin_name/route_name')
        def route_name(self):
            return 'Hello World!'
        ```

        Going to `plugin_name/route_name` would display the text `Hello World!`

        This can be used to create ReSTfull apis or new webpages entirely.
        """

        pass
