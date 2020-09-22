

def check_migration(settings: dict) -> bool:
    """
    Check if the settings should be migrated

    :param settings: Settings to migrate

    :return: whether the settings need to be migrated
    """
    return 'secret_key' in settings


def migrate(settings: dict) -> dict:
    """
    Migrate from the original settings to version 1 settings
    """
    web = settings.get('web', {})

    databases = web.get('databases', {})

    database = databases.get('default')
    if database is None:
        database = next(iter(databases.values()), None)

    api_keys = dict(
        (key.get('name'), {
            'key': key.get('key'),
            'permissions': key.get('permissions')
        })
        for key in web.get('api_keys', [])
    )

    new_settings = {
        'web': {
            'debug': settings.get('debug', False),
            'time_zone': settings.get('time_zone'),
            'allowed_hosts': web.get('allowed_hosts'),
            'database': database,
            'secret_key': settings.get('secret_key'),
            'sidebar': web.get('sidebar'),
            'api_keys': api_keys
        },
        'system': {
            'commands': settings.get('commands', {})
        },
        'plugins': settings.get('extensions'),
        'version': 1
    }
    return new_settings
