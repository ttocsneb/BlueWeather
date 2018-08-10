from blueweather import weather


class Weather:

    def __init__(self):
        self._table = weather.TableContainer()

    @property
    def table(self) -> weather.TableContainer:
        return self._table

    def getWeather(self) -> dict:
        return self._table._getTableDict()
