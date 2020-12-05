from blueweather.plugins.apps.config import Settings


class TestSettings(Settings):
    version = 1

    def get_interface(self):
        return {
            'settings': [
                {
                    'name': 'foo',
                    'type': 'number',
                    'default': '5'
                },
                {
                    'name': 'bar',
                    'type': 'text',
                    'default': 'cheese'
                }
            ],
            'items': [
                {
                    'type': 'setting',
                    'value': 'foo'
                },
                {
                    'type': 'setting',
                    'value': 'bar'
                }
            ]
        }

    def migrate(self, data: dict, version: int) -> dict:
        if version < 1:
            data = {
                'foo': 5,
                'bar': 'cheese'
            }
        return data

    def ready(self):
        pass
