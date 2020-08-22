from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'blueweather.apps.accounts'
    label = 'blueweather.apps.accounts'
    verbose_name = 'Account'
    icon = 'fas fa-user'

    def route(self, request):
        if request.user.is_authenticated:
            return 'profile'
        return 'login'

    def display_name(self, request):
        if request.user.is_authenticated:
            return request.user.username
        return "Login"

    def sidebar_items(self, request):
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
