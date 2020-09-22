import logging
from . import migrate_orig

migrations = [
    migrate_orig
]


def clear_empty_settings(settings: dict):
    """
    Clear the empty settings.

    Empty settings are any value that is set to :code:`None`

    :param settings: settings
    """
    if settings is None:
        return
    for key, setting in list(settings.items()):
        if setting is None:
            del settings[key]
        elif isinstance(setting, dict):
            clear_empty_settings(setting)


def migrate_settings(settings: dict) -> (dict, bool):
    """
    Migrate the settings

    :param settings: Settings to migrate

    :return: migrated settings, if settings were migrated
    """
    logger = logging.getLogger(__name__)

    migrated = False

    for migration in migrations:
        if not migration.check_migration(settings):
            continue
        logger.info(
            "Migrating Settings [%s]",
            migration.__name__.split('.')[-1]
        )
        migrated = True
        settings = migration.migrate(settings)
        clear_empty_settings(settings)

    if migrated:
        logger.info("Finished Migration")

    return settings, migrated
