import os

from django.conf import settings
from yapsy.IPluginLocator import IPluginLocator


class AppPluginLocator(IPluginLocator):
    """
    Locate plugins in the app
    """
    plugin_directory = os.path.join(settings.DATA_DIRECTORY, "plugins")

    def locatePlugins(self):
        """
        Walk through the plugins' places and look for plugins.

        Return the discovered plugins as a list of
        ``(candidate_infofile_path, candidate_file_path,plugin_info_instance)``
        and their number.
        """

    def gatherCorePluginInfo(self, directory, filename):
        """
        Return a ``PluginInfo`` as well as the ``ConfigParser`` used to build
        it.

        If filename is a valid plugin discovered by any of the known
        strategy in use. Returns None,None otherwise.
        """


class AppPluginDownloader:
    """
    Plugin Downloader will download and install plugins to a specific directory
    """
    download_directory = os.path.join(settings.DATA_DIRECTORY, "plugins")
    temp_directory = os.path.join(download_directory, "temp")

    def __init__(self, repository: str):
        """
        Load the downloader for a specific repository.

        :param str repository: a zip download link
        """
        self._repository = repository

    def download(self):
        """
        Download the plugin
        """
        raise NotImplementedError("This function has not yet been implemented")

    def install(self):
        """
        Install the plugin
        """
        raise NotImplementedError("This function has not yet been implemented")
