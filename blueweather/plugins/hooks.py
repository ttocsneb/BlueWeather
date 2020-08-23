

class Hook:
    def __init__(self, name: str):
        self.__name = name
        self.__hooks = dict()

    @property
    def name(self) -> str:
        return self.__name

    def call(self, *args, **kwargs):
        for hook in self.__hooks.values():
            hook(*args, **kwargs)

    def request(self, *args, **kwargs) -> list:
        values = list()
        for hook in self.__hooks.values():
            values.append(hook(*args, **kwargs))
        return values

    def _register_hook(self, name: str, hook: callable):
        if name in self.__hooks:
            raise KeyError("{} is already a registered hook".format(name))
        self.__hooks[name] = hook

    def _unregister_hook(self, name: str):
        if name not in self.__hooks:
            raise KeyError("{} is not a registered hook".format(name))
        del self.__hooks[name]

    def __repr__(self):
        return "<Hook('{}')>".format(self.name)


__hooks = dict()


def get_hook(name) -> Hook:
    """
    Create a new hook and return it

    With a hook, you can interact with other plugins.

    This can be done in two ways:

    1. send a message to other hooked plugins
    2. Request a message from other hooking plugins.

    This function retrieves a hook allowing you to call all
    hooked functions.

    Names should always be unique, so to prevent the possibility
    of clashes, the name of the plugin should be used as part
    of the hook name, such as "foobar_hook"
    """
    if name in __hooks:
        return __hooks[name]

    __hooks[name] = Hook(name)

    return __hooks[name]


def register_hook(name: str, hook_name: str, hook: callable):
    """
    Register a hook with a new hooked function.

    It is important when using hooks to know the parameters and
    return types for specific types of hooks.

    Names should always be unique, so to prevent the possibility
    of clashes, the name of the plugin should be used as part
    of the hook name, such as "foobar_hook"
    """
    hook = get_hook(name)
    hook._register_hook(hook_name, hook)


def unregister_hook(name: str, hook_name: str):
    """
    Unregister a hooked function
    """
    hook = get_hook(name)
    hook._unregister_hook(hook_name)
