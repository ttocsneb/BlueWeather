import json


class StatusTable:

    def __init__(self, title=None, data=None):
        self._data = dict()

        if data:
            self._data = data
        else:
            self._data['data'] = list()

        if title:
            self._data['title'] = title

    @property
    def title(self) -> str:
        return self._data['title']

    @title.setter
    def title(self, value: str):
        self._data['title'] = str(value)

    @property
    def headers(self):
        if not self._data.get('header'):
            self._data['header'] = list()
        return self._data['header']

    @headers.setter
    def headers(self, headers: list):
        self._data['header'] = headers

    def setRowCategory(self, row: int, category=None):
        if category:
            self._data['data'][row]['category'] = category
        else:
            del self._data['data'][row]['category']

    def getRowCategory(self, row: int) -> str:
        return self._data['data'][row].get('category')

    def append(self, value):
        self._data['data'].append({'row': value})

    def extend(self, values):
        for x in values:
            self.append(x)

    def __getitem__(self, idx):
        return self._data['data'][idx].get('row')

    def __setitem__(self, idx, value):
        self._data['data'][idx]['row'] = value

    def __iter__(self):
        return iter([x['row'] for x in self._data['data']])

    @property
    def table(self):
        return self._data

    @table.setter
    def table(self, value):
        self._data = value


class Status:

    def __init__(self):
        self._status = {'messages': {}, 'data': {}}

    def setStatusMessage(self, key: str, message: str, category='info'):
        self._status['messages'][key] = [category, message]

    def updateStatusTable(self, key: str, data: StatusTable):
        self._status['data'][key] = data.table

    def loadStatusTable(self, key: str, data=None) -> StatusTable:
        table = self._status['data'][key]
        if data:
            data.table = table
            return data
        return StatusTable(table)

    def getJSONStatus(self):
        return json.dumps(self._status)

    def getStatus(self):
        return self._status
