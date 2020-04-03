import logging

_logger = logging.getLogger(__name__)


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
        return any(map(lambda x: x.modified, self._modifiable))

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


class Web(Settings):
    _required = []
    _defaults = dict(
        static_url="/static/"
    )

    def __init__(self, static_url: str = None):
        super().__init__()
        self.static_url = static_url or self._defaults['static_url']

        self._init = False


class Config(Settings):
    _required = ["secret_key"]
    _defaults = dict(
        debug=False,
        web=dict()
    )
    _modifiable = ["web"]

    def __init__(self, secret_key: str = None, debug: bool = None,
                 web: Web = None):
        super().__init__()
        self.secret_key = secret_key
        if self.secret_key is None:
            self.secret_key = generate_secret()
            self.modified = True

        self.debug = debug or self._defaults['debug']
        self.web = web
        if self.web is None:
            self.web = Web()

        self._init = False


