from django.apps import AppConfig
from django.conf import settings

from . import methods

from blueweather.plugins.apps.config import Settings


class TestSettings(Settings):
    version = 3

    def get_interface(self):
        return {
            'settings': [
                {
                    'name': 'bar',
                    'title': 'Bar',
                    'type': 'number'
                },
                {
                    'name': 'choice',
                    'title': 'Choice',
                    'type': 'select',
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
                },
                {
                    'name': 'check',
                    'title': 'Check',
                    'type': 'bool'
                },
                {
                    'name': 'radio',
                    'title': 'Radio',
                    'type': 'radio',
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
                },
                {
                    'name': 'many',
                    'title': 'Many',
                    'type': 'radio',
                    'choices': [
                        {
                            'key': 'q',
                            'value': 'Q'
                        },
                        {
                            'key': 'w',
                            'value': 'W'
                        },
                        {
                            'key': 'e',
                            'value': 'E'
                        },
                        {
                            'key': 'r',
                            'value': 'R'
                        },
                        {
                            'key': 't',
                            'value': 'T',
                        },
                        {
                            'key': 'y',
                            'value': 'Y'
                        }
                    ],
                    'multiple': True
                }
            ],
            'items': [
                {
                    'type': 'header',
                    'value': 'Settings Example'
                },
                {
                    'type': 'setting',
                    'value': 'bar'
                },
                {
                    'type': 'setting',
                    'value': 'choice'
                },
                {
                    'type': 'setting',
                    'value': 'check'
                },
                {
                    'type': 'divider'
                },
                {
                    'type': 'setting',
                    'value': 'radio'
                },
                {
                    'type': 'setting',
                    'value': 'many'
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
        if version == 2:
            version = 3
            data['many'] = ['q', 't']
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
