from blueweather.plugin import types

from blueweather.weather.status import StatusTable, Status


class TestPlugin(types.WeatherPlugin, types.StartupPlugin):

    def __init__(self):
        super(TestPlugin, self).__init__()

        self.table = StatusTable('Test Plugin Status')
        self.table.width = 2

        self.num = 0

        rows = [[str(x), "Hello World"] for x in range(5)]
        self.table.extend(rows)

    def on_after_startup(self):
        self._logger.info("Hello World!")

        for x in range(10):
            self._status.setStatusMessage(__name__ + str(x),
                                          "Message {0}!".format(x),
                                          closeable=True)

    def on_status_request(self):
        self._logger.info("Status is requested!")

        self.num += 1

        self._status.setStatusMessage(__name__ + 'status',
                                      "An updating status {0}".format(self.num))

        self._status.updateStatusTable(__name__, self.table)
