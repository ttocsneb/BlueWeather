from django.conf import settings

from blueweather.plugins import Extensions, dao

from typing import List


def pageify(items: list, page_size: int) -> list:
    """
    Convert a list of items into pages

    :param items: the items to convert
    :param page_size: the number of items per page

    :return: list of pages
    """
    return [
        items[i:i + page_size]
        for i in range(0, len(items), page_size)
    ]


def plugin_list() -> List[dict]:
    """
    Get a list of all the plugins as a json list.

    .. note::

        The shown parameters are GET parameters

    :return: List of plugins

        .. code-block:: ts

            interface Plugin {
                pluginName: string
                enabled: boolean
                extensions: Array<string>
                info: {
                    packageName: string
                    version?: string
                    summary?: string
                    homepage?: string
                    author?: string
                    email?: string
                    license?: string
                    description?: html
                }
            }

            type PluginList = Array<Plugin>

    """
    extensions: Extensions = settings.EXTENSIONS

    plugins = extensions.getAllExtensions()

    out = []

    for name, exts in plugins.items():
        ext = list(exts.values())[0]
        out.append({
            'pluginName': name,
            'info': dao.PluginInfo.get_metadata(ext),
            'enabled': extensions.is_enabled(ext),
            'builtin': ext.builtin,
            'extensions': [
                k for k in exts.keys()
            ],
        })

    return out
