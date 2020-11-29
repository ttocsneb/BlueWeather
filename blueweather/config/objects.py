import logging
import os

_logger = logging.getLogger(__name__)


def _print_attrs(obj, *args, join="\n  "):
    import pprint
    attr_list = ['{} = {}'.format(i, pprint.pformat(getattr(obj, i)))
                 for i in sorted(args)]
    split = ',\n'.join(attr_list).split('\n')
    return join + join.join(split)


def generate_key(alphabet, length=50):
    """
    > Inspired from https://gist.github.com/ndarville/3452907

    Generate a secret key using systemrandom
    """
    import random

    _logger.info("Generating Secret Key..")

    SECRET_KEY = ''.join(
        [random.SystemRandom().choice(alphabet)
         for i in range(length)
         ]
    )
    return SECRET_KEY


def generate_secret():
    return generate_key('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')


def generate_api():
    return generate_key('1234567890abcdef', length=32)


class Settings:
    """
    Settings will store changes to the object in the variable `modified`. This
    can be used to check whether the settings need to be written to disk.
    """

    def __init__(self):
        self._modified = False

    @property
    def modified(self):
        """
        Is this object or any of its children modified?
        """
        if self._modified:
            return True
        return any(map(lambda x: x.modified, self._modifiable.values()))

    @property
    def _modifiable(self) -> dict:
        """
        Get the children that are modifiable
        """
        modifiable = dict()
        for key, value in self.__dict__.items():
            if hasattr(value, 'modified'):
                modifiable[key] = value
        return modifiable

    @modified.setter
    def modified(self, value):
        self._modified = value
        if not value:
            for m in self._modifiable.values():
                m.modified = False


class Database(Settings, dict):
    def __init__(self, engine: str = None, name: str = None, path: str = None,
                 **kwargs):
        super().__init__()

        self["ENGINE"] = engine or 'sqlite3'
        if name is None and path is None:
            path = "db.sqlite3"
        if path is not None:
            self['PATH'] = path
        elif name is not None:
            self['NAME'] = name

        for k, v in kwargs.items():
            self[k.upper()] = v

    def get_data(self, base_dir) -> dict:
        """
        Get the final data ready for DATABASES Settings
        """
        final = dict(self)
        if 'PATH' in final:
            if not os.path.isabs(final['PATH']):
                final['PATH'] = os.path.join(base_dir, final['PATH'])
            final['NAME'] = final['PATH']
            del final['PATH']
        return final


class ApiKey(Settings):
    def __init__(self, key: str = None, permissions: list = None):
        self.key = key
        if self.key is None:
            self.key = generate_api()
        self.permissions = permissions or []

    def check(self, other: str) -> bool:
        """
        Check if the key is equivalent to the other key

        :param other: other key

        :return: whether the keys are equal
        """
        return other.replace('-', '').lower() == \
            self.key.replace('-', '').lower()


class ApiKeys(dict, Settings):
    def find(self, key: str) -> (str, ApiKey):
        """
        Search for an api key with a matching key

        :param key: key to look for

        :return: name, ApiKey
        """
        for k, v in self.items():
            if v.check(key):
                return k, v
        return None, None


class Web(Settings):
    def __init__(self, debug: bool = False, time_zone: str = None,
                 allowed_hosts: list = None, database: Database = None,
                 secret_key: str = None, sidebar: list = None,
                 api_keys: list = None, frontend: str = None,
                 calculate_secret: bool = True):
        super().__init__()

        self.debug = debug or False
        self.time_zone = time_zone or "UTC"

        self.secret_key = secret_key
        if self.secret_key is None and calculate_secret:
            self.secret_key = generate_secret()
            self.modified = True

        self.database = database
        if self.database is None:
            self.database = Database()
            self._modified = True

        self.allowed_hosts = allowed_hosts or ['*']

        self.api_keys = ApiKeys(**(api_keys or {}))

        self.frontend = frontend or "frontend"

        self.sidebar = sidebar
        if self.sidebar is None:
            self.sidebar = [
                {
                    "category": "item",
                    "value": "plugins"
                },
                {
                    "category": "item",
                    "value": "settings"
                },
                {
                    "category": "item",
                    "value": "accounts"
                }
            ]
            self._modified = True

    def __repr__(self):
        return str(self)


class Plugins(Settings):
    def __init__(self, weather_driver: str = None, enabled: list = None):
        super().__init__()

        self.weather_driver = weather_driver or 'dummyWeather'

        self.enabled = enabled or ['blueweather.plugins.integrated.dummyWeather']


class Apps(Settings):
    def __init__(self, settings: dict = None):
        self.settings = settings or dict()


class System(Settings):
    def __init__(self, commands: dict = None):
        super().__init__()

        self.commands = commands or dict()


class Config(Settings):
    def __init__(self, web: Web = None, system: System = None,
                 plugins: Plugins = None, apps: Apps = None,
                 version: int = None, calculate_secret: bool = True):
        super().__init__()

        self.web = web
        if self.web is None:
            self.web = Web(calculate_secret=calculate_secret)

        self.system = system
        if self.system is None:
            self.system = System()

        self.plugins = plugins
        if self.plugins is None:
            self.plugins = Plugins()

        self.apps = apps
        if self.apps is None:
            self.apps = Apps()

        self.version = version or 2
