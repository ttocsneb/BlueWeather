from django.contrib.auth.models import User


def get_user_data(user: User):
    """
    Get the userdata from the user

    :param user: user

    :return: userdata for the client
    """

    if user.is_anonymous:
        name = None
    else:
        name = user.get_full_name() or user.get_username()

    return {
        'username': user.get_username(),
        'name': name,
        'is_active': user.is_active,
        'is_anonymous': user.is_anonymous,
        'is_authenticated': user.is_authenticated,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'last_login': None if user.is_anonymous else user.last_login
    }
