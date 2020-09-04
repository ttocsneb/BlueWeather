from django.apps import AppConfig
from django.http import HttpRequest


class AccountsConfig(AppConfig):
    name = 'blueweather.apps.accounts'
    label = 'blueweather.apps.accounts'
    verbose_name = 'Account'
    icon = 'fas fa-user'

    def route(self, request: HttpRequest) -> str:
        """
        Get the route for the sidebar

        :param request: request

        :return: `profile` or `login` if not logged in
        """
        if request.user.is_authenticated:
            return 'profile'
        return 'login'

    def display_name(self, request: HttpRequest) -> str:
        """
        Get the name of the sidebar item

        :param request: request

        :return: :code:`request.user.username` or `Login` if not logged in
        """
        if request.user.is_authenticated:
            return request.user.username
        return "Login"

    def sidebar_items(self, request: HttpRequest):
        """
        Get the child menu items

        :param request: request

        :return: list of user actions if logged in
        """
        if request.user.is_authenticated:
            return [
                {
                    "category": "item",
                    "value": {
                        "display_name": "Profile",
                        "route": "profile"
                    }
                },
                {
                    "category": "item",
                    "value": {
                        "display_name": "Change Password",
                        "route": "password_change"
                    }
                },
                {
                    "category": "divider"
                },
                {
                    "category": "item",
                    "value": {
                        "display_name": "Logout",
                        "route": "logout"
                    }
                }
            ]
        return None
