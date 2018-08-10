from blueweather.plugin import types

from blueweather.weather import Table


class TestPlugin(types.WeatherPlugin, types.StartupPlugin):

    def __init__(self):
        super(TestPlugin, self).__init__()

        self.table = Table('Test Plugin Status')
        self.table.width = 4

        self.num = 0

        rows = [[str(x), "Hello World"] for x in range(10)]
        self.table.extend(rows)

    def on_after_startup(self):
        self._logger.info("Hello World!")

        for x in range(2):
            self._status.setStatusMessage(__name__ + str(x),
                                          "Message {0}!".format(x),
                                          closeable=True)

        self._logger.info(self.table.table)

    def on_status_request(self):
        self._logger.info("Status is requested!")

        self.num += 1

        self._status.setStatusMessage(__name__ + 'status',
                                      "An updating status {0}".format(self.num)
                                      )

        self._status.table[__name__] = self.table
        self._status.table['Foo'] = self.table
