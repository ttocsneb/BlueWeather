from blueweather.plugin import types

from blueweather.weather.status import StatusTable, Status


class TestPlugin(types.WeatherPlugin):

    def __init__(self):
        super(TestPlugin, self).__init__()

        self.number = 0

        self.table = StatusTable('Test Plugin Status')
        self.table.width = 2

        rows = [[str(x), "Hello World"] for x in range(5)]
        self.table.extend(rows)

    def on_status_request(self):
        self._logger.info("Status is requested!")

        self.number += 1

        self._status.setStatusMessage(str(self.number), "A new Message!")

        self._status.updateStatusTable(__name__, self.table)
