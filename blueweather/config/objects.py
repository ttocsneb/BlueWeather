import logging
import os

_logger = logging.getLogger(__name__)


def _print_attrs(obj, *args, join="\n  "):
    import pprint
    attr_list = ['{} = {}'.format(i, pprint.pformat(getattr(obj, i)))
                 for i in sorted(args)]
    split = ',\n'.join(attr_list).split('\n')
    return join + join.join(split)


def generate_secret():
    """
    > Inspired from https://gist.github.com/ndarville/3452907

    Generate a secret key using systemrandom
    """
    import random

    _logger.info("Generating Secret Key..")

    SECRET_KEY = ''.join(
        [random.SystemRandom().choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
         for i in range(50)
         ]
    )
    return SECRET_KEY


class Settings:
    """
    Settings will store changes to the object in the variable `modified`. This
    can be used to check whether the settings need to be written to disk.
    """

    _defaults = dict()
    _required = list()
    _modifiable = list()

    def __init__(self):
        self._init = True
        self._modified = False

    @property
    def modified(self):
        """
        Is this object or any of its children modified?
        """
        if self._modified:
            return True
        return any(map(lambda x: getattr(self, x).modified, self._modifiable))

    def __is_setting(self, name):
        return name in self._defaults.keys() or name in self._required

    @modified.setter
    def modified(self, value):
        super().__setattr__("_modified", value)
        if not value:
            for m in self._modifiable:
                if not hasattr(self, m):
                    continue
                getattr(self, m).modified = False

    def __setattr__(self, name, value):
        """
        Log any changes made to the Setting object.
        If there were changes made, modifed will be set to true
        """
        if self.__is_setting(name) and not self._init \
                and getattr(self, name) != value:
            super().__setattr__("_modifed", True)
        return super().__setattr__(name, value)


class Database(Settings, dict):
    _required = ['engine']
    _defaults = dict(
        engine="sqlite3"
    )

    def __init__(self, engine: str = None, name: str = None, path: str = None,
                 **kwargs):
        super().__init__()

        self["ENGINE"] = engine or self._defaults['engine']
        if name is None and path is None:
            path = "db.sqlite3"
        if path is not None:
            self['PATH'] = path
        elif name is not None:
            self['NAME'] = name

        for k, v in kwargs.items():
            self[k.upper()] = v
        self._init = False

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


class Web(Settings):
    _required = []
    _defaults = dict(
        static_url="/static/",
        allowed_hosts=[]
    )
    _modifiable = []

    def __init__(self, static_url: str = None, databases: dict = None,
                 password_validation: dict = None, allowed_hosts: list = None,
                 template_globals: dict = None, sidebar: list = None):
        super().__init__()
        self.static_url = static_url or self._defaults['static_url']

        self.databases = databases
        if self.databases is None:
            self.databases = dict(default=Database())
            self._modified = True

        self.password_validation = password_validation
        if self.password_validation is None:
            base = 'django.contrib.auth.password_validation'
            self.password_validation = [
                dict(NAME='{}.UserAttributeSimilarityValidator'.format(base)),
                dict(NAME='{}.MinimumLengthValidator'.format(base)),
                dict(NAME='{}.CommonPasswordValidator'.format(base)),
                dict(NAME='{}.NumericPasswordValidator'.format(base))
            ]
            self._modified = True

        self.allowed_hosts = allowed_hosts or self._defaults['allowed_hosts']

        self.template_globals = template_globals
        if self.template_globals is None:
            self.template_globals = dict(title="BlueWeather")
            self._modified = True

        self.sidebar = sidebar

        self._init = False

    def __str__(self):
        data = _print_attrs(
            self,
            'static_url', 'databases', 'password_validation', 'allowed_hosts'
        )

        return "Web{%s\n}" % data

    def __repr__(self):
        return str(self)


class Config(Settings):
    _required = ["secret_key"]
    _defaults = dict(
        debug=False,
        web=dict(),
        time_zone="UTC"
    )
    _modifiable = ["web"]

    def __init__(self, secret_key: str = None, debug: bool = None,
                 web: Web = None, time_zone: str = None):
        super().__init__()
        self.secret_key = secret_key
        if self.secret_key is None:
            self.secret_key = generate_secret()
            self.modified = True

        self.debug = debug or self._defaults['debug']
        self.time_zone = time_zone or self._defaults['time_zone']
        self.web = web
        if self.web is None:
            self.web = Web()

        self._init = False

    def __str__(self):
        data = _print_attrs(self, "debug", "time_zone", "web")
        return "Config{%s\n}" % data

    def __repr__(self):
        return str(self)
