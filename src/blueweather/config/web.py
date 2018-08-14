
# import the secrets module, use os.urandom if running <3.5
try:
    from secrets import token_hex
except ImportError:
    from os import urandom

    def token_hex(nbytes=None):
        return urandom(nbytes).hex()

from .database import Database


class WebConfig:

    def __init__(self, secret_key=None, database=None, host=None, port=None):
        if not secret_key:
            secret_key = token_hex(16)

        if not database:
            database = Database()

        if not host:
            host = '0.0.0.0'

        if not port:
            port = 5000

        self.secret_key = str(secret_key)
        self.database = database
        self.host = str(host)
        self.port = int(port)

    def getObject(self) -> dict:
        obj = dict()
        obj['secret_key'] = self.secret_key
        obj['database'] = self.database.getObject()
        return obj

    @staticmethod
    def loadObject(obj: dict):
        # Convert the database dict to a Database Object
        if 'database' in obj and not isinstance(obj['database'], Database):
            print(obj)
            print(obj['database'])
            db = Database.loadObject(obj['database'])
            obj['database'] = db
        return WebConfig(**obj)
