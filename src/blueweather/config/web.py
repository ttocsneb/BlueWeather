
# import the secrets module, use os.urandom if running <3.5
try:
    from secrets import token_hex
except ImportError:
    from os import urandom

    def token_hex(nbytes=None):
        return urandom(nbytes).hex()

from .database import Database


class WebConfig:

    def __init__(self, secret_key=None, database=None, host=None, port=None, home_page=None):
        if not secret_key:
            secret_key = token_hex(16)

        if not database:
            database = Database()

        if not host:
            host = '0.0.0.0'

        if not port:
            port = 5000

        if not home_page:
            home_page = '/dashboard'

        self.secret_key = str(secret_key)
        self.database = database
        self.host = str(host)
        self.port = int(port)
        self.home_page = str(home_page)

    def getObject(self) -> dict:
        obj = dict()
        obj['secret_key'] = self.secret_key
        obj['host'] = self.host
        obj['port'] = self.port
        obj['home_page'] = self.home_page
        obj['database'] = self.database.getObject()
        return obj

    @staticmethod
    def loadObject(obj: dict):
        # Convert the database dict to a Database Object
        if 'database' in obj and not isinstance(obj['database'], Database):
            db = Database.loadObject(obj['database'])
            obj['database'] = db
        return WebConfig(**obj)
