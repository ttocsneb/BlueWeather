from django.apps import AppConfig


class TestSettingsConfig(AppConfig):
    name = 'test_plugins.settings'
    label = 'test_settings'

    description = """A Test Settings plugin.

    This test plugin tests the integration of settings.
    """

    summary = description.splitlines()[0]
