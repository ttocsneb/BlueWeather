from django.apps import AppConfig
from django.conf import settings

from . import methods

from blueweather.plugins.apps.config import Settings


class TestSettings(Settings):
    version = 2

    def get_interface(self):
        return {
            'settings': [
                {
                    'name': 'bar',
                    'type': 'number'
                },
                {
                    'name': 'choice',
                    'type': 'select',
                    'options': {
                        'choices': [
                            {
                                'key': 'a',
                                'value': "A"
                            },
                            {
                                'key': 'b',
                                'value': 'B'
                            },
                            {
                                'key': 'c',
                                'value': 'C'
                            }
                        ]
                    }
                },
                {
                    'name': 'check',
                    'type': 'bool'
                },
                {
                    'name': 'radio',
                    'type': 'radio',
                    'options': {
                        'choices': [
                            {
                                'key': 'jeff',
                                'value': 'Jeff'
                            },
                            {
                                'key': 'bar',
                                'value': 'Bar'
                            },
                            {
                                'key': 'yeet',
                                'value': 'YEET'
                            }
                        ]
                    }
                }
            ],
            'items': [
                {
                    'type': 'header',
                    'value': 'Settings Example'
                },
                {
                    'type': 'label',
                    'value': 'Bar'
                },
                {
                    'type': 'setting',
                    'value': 'bar'
                },
                {
                    'type': 'label',
                    'value': 'Choice'
                },
                {
                    'type': 'setting',
                    'value': 'choice'
                },
                {
                    'type': 'label',
                    'value': 'Check'
                },
                {
                    'type': 'setting',
                    'value': 'check'
                },
                {
                    'type': 'divider'
                },
                {
                    'type': 'label',
                    'value': 'Radio'
                },
                {
                    'type': 'setting',
                    'value': 'radio'
                }
            ]
        }

    def migrate(self, data, version):
        if version == 0:
            version = 1
            data['bar'] = 5
            data['choice'] = 'a'
            data['check'] = False
        if version == 1:
            version = 2
            data['radio'] = 'jeff'
        return data

    def ready(self):
        print("The Test Settings are Ready!")


class SettingsConfig(AppConfig):
    name = 'blueweather.apps.settings'
    label = 'settings'
    verbose_name = 'Settings'
    icon = 'fas fa-cog'
    route = 'settings:index'
    login_required = True

    api = 'blueweather.apps.settings.api'

    settings = TestSettings

    def ready(self):
        ready_settings = methods.initialize()
        if settings.CONFIG.modified:
            settings.CONFIG.save()

        for conf in ready_settings:
            conf.ready()
