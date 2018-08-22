import signal
from contextlib import contextmanager
import logging

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import FallbackHandler, RequestHandler, Application


logger = logging.getLogger(__name__)


class MainHandler(RequestHandler):
    def get(self):
        self.write("This message comes from Tornado ^_^")


def on_shutdown():
    logger.info("Stopping the Server")
    IOLoop.instance().stop()


@contextmanager
def sigint_shutdown(ioloop):
    """
    Overrides the current sigint signal to stop the tornado server.  This
    should be used with the ``with`` command on ``ioloop.start()``

    :param AsyncIOMainLoop ioloop: IOLoop.instance()
    """
    original_sigint_handler = signal.getsignal(signal.SIGINT)
    signal.signal(
        signal.SIGINT,
        lambda sig, frame: ioloop.add_callback_from_signal(on_shutdown)
    )
    try:
        logger.info("Press Ctrl-C to stop the server")
        yield
    except:
        raise
    finally:
        logger.debug("Returning control to default signal handler")
        signal.signal(signal.SIGINT, original_sigint_handler)


counter = 0


def heartbeat():
    global counter
    counter += 1
    if counter >= 300:
        logger.info("Heartbeat <3")
        counter = 0


def startServer(host, port, app):
    ioloop = IOLoop.instance()

    tr = WSGIContainer(app)

    application = Application([
        (r"/tornado", MainHandler),
        (r".*", FallbackHandler, dict(fallback=tr)),
    ])

    application.listen(port, address=host)

    # The heartbeat allows the sigint signal (Ctrl-C) to be processed.
    periodic_heartbeat = PeriodicCallback(heartbeat, 1000)
    periodic_heartbeat.start()

    with sigint_shutdown(ioloop):
        ioloop.start()
