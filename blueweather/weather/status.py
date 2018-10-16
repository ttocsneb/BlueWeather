from blueweather import weather


class Status:

    def __init__(self):
        self._status = dict()
        self._status['messages'] = dict()
        self._status['data'] = dict()

        self._table = weather.TableContainer()

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

    @property
    def table(self) -> weather.TableContainer:
        return self._table

    def getStatus(self) -> dict:
        """
        Get a dict representing the status

        :return dict: status
        """
        self._status['tables'] = self._table._getTableDict()
        return self._status
