from stringlike import StringLike
import json


class JsonEncoder(json.encoder.JSONEncoder):
    """
    A JsonEncoder that handles stringlikes
    """
    def default(self, obj):
        if isinstance(obj, StringLike):
            return str(obj)
        return super().default(obj)
