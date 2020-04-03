from blueweather import weather


class Weather:

    def __init__(self):
        self._data = dict()
        self._table = weather.TableContainer()

    @property
    def table(self) -> weather.TableContainer:
        return self._table

    def getWeather(self) -> dict:
        self._data['tables'] = self._table._getTableDict()
        return self._data
