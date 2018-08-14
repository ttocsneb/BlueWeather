
class Database:

    def __init__(self, uri='sqlite:///site.db', track_modifications=False):
        self.uri = uri
        self.track_modifications = track_modifications

    def getObject(self) -> dict:
        obj = dict()
        obj['uri'] = self.uri
        obj['track_modifications'] = self.track_modifications
        return obj

    @staticmethod
    def loadObject(obj: dict):
        return Database(**obj)
