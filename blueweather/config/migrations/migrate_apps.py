

def check_migration(settings: dict) -> bool:
    """
    Check if the settings should be migrated

    :param settings: Settings to migrate

    :return: whether the settings need to be migrated
    """
    return settings['version'] == 1


def migrate(settings: dict) -> dict:
    """
    Migrate from version 1 settings to version 2
    """
    # Move plugin settings to app settings

    settings['apps'] = {
        'settings': settings.get('plugins', {}).get('settings', {})
    }

    if 'plugins' in settings:
        plugins = settings['plugins']
        if 'settings' in plugins:
            del plugins['settings']

    settings['version'] = 2
    return settings
