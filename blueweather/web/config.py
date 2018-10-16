
from blueweather import variables


class Config:

    def __init__(self):
        self.SECRET_KEY = variables.config.web.secret_key
        self.SQLALCHEMY_DATABASE_URI = variables.config.web.database.uri
        self.SQLALCHEMY_TRACK_MODIFICATIONS = \
            variables.config.web.database.track_modifications
