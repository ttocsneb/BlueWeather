import json


class StatusTable:
    """
    The StatusTable allows you to easily create a table used for status
    messages

    This is an iterable object.
    """

    def __init__(self, title=None, data=None):
        self._data = dict()

        self.width = 6
        self.table = data

        if title:
            self._data['title'] = title

    @property
    def title(self) -> str:
        return self._data['title']

    @title.setter
    def title(self, value: str):
        self._data['title'] = str(value)

    @property
    def width(self):
        return self._data['width']

    @width.setter
    def width(self, value):
        self._data['width'] = value

    @property
    def headers(self):
        if not self._data.get('header'):
            self._data['header'] = list()
        return self._data['header']

    @headers.setter
    def headers(self, headers: list):
        self._data['header'] = headers

    def setRowCategory(self, row: int, category=None):
        """
        Set or remove the Category for a row

        :param int row: row to set category

        :param str category: category to set, remove if None
            primary
            secondary
            success
            danger
            warning
            info
            light
            dark
        """
        if category:
            self._data['data'][row]['category'] = category
        else:
            del self._data['data'][row]['category']

    def getRowCategory(self, row: int) -> str:
        """
        Get the category of a row

        :param int row: row to get category from

        :return str: category or None if not set
        """
        return self._data['data'][row].get('category')

    def append(self, value: list):
        """
        Add a row to the table

        :param list value: row to add
        """
        self._data['data'].append({'row': value})

    def extend(self, values: list):
        """
        Add a number of rows to the table

        :param list(list) values: a list of rows to add
        """
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
        if value:
            self._data = value
        else:
            self._data = dict()
            self._data['data'] = list()


class Status:

    def __init__(self):
        self._status = {'messages': {}, 'data': {}}

    def setStatusMessage(self, key: str, message=None, category='info',
                         closeable=False):
        """
        Create or remove a status message.  The key should be unique to your
        plugin.  You may have more than one Status message if you like.

        :param str key: a unique key for the message

        :param str message: a message to display.  If ``None`` any existing
        message will be removed

        :param str category: a bootstrap category the options are
            primary
            secondary
            success
            danger
            warning
            info
            light
            dark

        :param bool closeable: true if the client can close the message
        """
        if message:
            self._status['messages'][key] = [category, message, closeable]
        elif key in self._status['messages']:
            del self._status['messages'][key]

    def updateStatusTable(self, key: str, data=None):
        """
        Update or remove a status table.  The key should be unique to your
        plugin.  You may have more than one status table if you like

        :param str key: a unique key for the table

        :param StatusTable data: a Status table object.  If ``None``, any
        existing table will be removed
        """
        if data:
            self._status['data'][key] = data.table
        elif key in self._status['data']:
            del self._status['data'][key]

    def loadStatusTable(self, key: str, data=None) -> StatusTable:
        """
        Load an existing Status table into a ``StatusTable`` object

        if ``data`` is provided, then the table will be loaded into that

        If there is no ``StatusTable`` for the provided key, then an empty
        ``StatusTable`` will be created

        :param str key: key

        :param StatusTable data: table to load found status table into

        :return StatusTable: the found StatusTable, ``data`` if provided
        """
        table = self._status['data'].get(key)
        if data:
            data.table = table
            return data
        return StatusTable(data=table)

    def getJSONStatus(self) -> str:
        """
        Get the JSON object representing the status

        :return str: status JSON object
        """
        return json.dumps(self._status)

    def getStatus(self) -> dict:
        """
        Get a dict representing the status

        :return dict: status
        """
        return self._status
