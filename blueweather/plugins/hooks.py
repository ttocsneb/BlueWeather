import inspect
import logging


class Hook:
    """
    Holds all the functions that are subscribed to this hook.
    """

    def __init__(self, name: str, signature: inspect.Signature):
        self.__name = name
        self.__hooks = dict()
        self.__signature = signature

    @property
    def name(self) -> str:
        """
        Name of the hook
        """
        return self.__name

    def call(self, *args, **kwargs):
        """
        Call all the hooked functions without retreiving the return value

        :param args: positional arguments
        :param kwargs: keyword arguments
        """
        bound = self.__signature.bind(*args, **kwargs)
        for name, hook in self.__hooks.items():
            try:
                hook(*bound.args, **bound.kwargs)
            except Exception:
                logging.getLogger(__name__).exception(
                    "An error occurred while processing the hook %s:%s",
                    self.name, name
                )

    def request(self, *args, **kwargs) -> list:
        """
        Call all the hooked functions, and return a list of returned values

        :param args: positional arguments
        :param kwargs: keyword arguments

        :return: list of return values
        """
        bound = self.__signature.bind(*args, **kwargs)
        values = list()
        for hook in self.__hooks.values():
            try:
                values.append(hook(*bound.args, **bound.kwargs))
            except Exception:
                logging.getLogger(__name__).exception(
                    "An error occurred while processing the hook %s:%s",
                    self.name, name
                )

        return values

    def subscribe(self, name: str, func: callable):
        """
        Subscribe to the hook

        When the hook is called, the function will be called

        .. note::

            The name should be unique, so to help prevent collisions,
            add/use the plugin name (`simplePlugin`)

        :param name: name of the subscriber
        :parm func: function to subscribe
        """
        if name in self.__hooks:
            raise KeyError("{} is already subscribed".format(name))
        self.__hooks[name] = func

    def unsubscribe(self, name: str):
        """
        Unsubscribe from the hook

        :param name: name of the subscriber
        """
        if name not in self.__hooks:
            raise KeyError("{} is not subscribed".format(name))
        del self.__hooks[name]

    def __repr__(self):
        return "<Hook('{}')>".format(self.name)


__hooks = dict()


def get_hook(name) -> Hook:
    """
    Create or retrieve a hook

    With hooks, you can interact with other plugins in one of two ways

    1. Send a message to other subscribed plugins
    2. Subscribe to a hook that anyone can call.

    Names should always be unique, so to prevent the possibility
    of clashes, the name of the plugin should be used as part
    of the hook name, such as "simplePlugin_hookName"

    :return: hook
    """
    if name in __hooks:
        return __hooks[name]

    __hooks[name] = Hook(name)

    return __hooks[name]
