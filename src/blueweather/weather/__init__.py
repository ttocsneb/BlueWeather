"""
Acts as the programs interface between the server and the weatherstation.
"""


class Table:
    """
    The Table allows you to easily create a table used for status
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
    def table(self) -> dict:
        return self._data

    @table.setter
    def table(self, value):
        if value:
            self._data = value
        else:
            self._data = dict()
            self._data['data'] = list()


class TableContainer:
    """
    An internal class used by ``weather.status.Status``,
    and ``weather.weather.Weather`` that contains the ``Table`` object.
    """

    def __init__(self):
        self._table = dict()

    def remove(self, key):
        if key in self._table:
            del self._table[key]

    def get(self, key, default=None):
        return self._table.get(key, default)

    def __getitem__(self, key) -> Table:
        return Table(data=self._table[key])

    def __setitem__(self, key, value: Table):
        if isinstance(value, Table):
            self._table[key] = value.table
        else:
            raise TypeError()

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self._table[k] = v

    def _getTableDict(self) -> dict:
        return self._table
