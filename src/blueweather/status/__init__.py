import json

_status = {'messages': {}, 'data': {}}


class StatusTable:

    def __init__(self, title: str):
        self._data = dict()

        self._data['title'] = title
        self._data['data'] = list()

    def addRow(self, columns: list, category=None):
        row = dict()
        row['row'] = columns
        if category:
            row['category'] = category
        self._data['data'].append(row)

    def setRow(self, row: int, columns=None, category=None):
        if columns:
            self._data['data'][row]['row'] = columns
        if category:
            self._data['data'][row]['category'] = category

    def setValue(self, row: int, col: int, value):
        self._data['data'][row]['row'][col] = value

    def setHeaders(self, headers: list):
        self._data['header'] = headers

    def setHeader(self, col: int, header: str):
        self._data['header'][col] = header

    def getValue(self, row: int, col: int) -> str:
        return self._data['data'][row]['row'][col]

    @property
    def table(self):
        return self._data


def setStatusMessage(key: str, message: str, category='info'):
    _status['messages'][key] = [category, message]


def updateStatusTable(key: str, data: StatusTable):
    _status['data'][key] = data.table


def getJSONStatus():
    return json.dumps(_status)


def getStatus():
    return _status
