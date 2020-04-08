from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'blueweather.accounts'
    label = 'blueweather.accounts'
    verbose_name = 'Account'
    icon = 'fas fa-user'

    def route(self, request):
        if request.user.is_authenticated:
            return 'accounts:profile'
        return 'accounts:login'

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
                        "route": "accounts:profile"
                    }
                },
                {
                    "category": "item",
                    "value": {
                        "display_name": "Change Password",
                        "route": "accounts:password_change"
                    }
                },
                {
                    "category": "divider"
                },
                {
                    "category": "item",
                    "value": {
                        "display_name": "Logout",
                        "route": "accounts:logout"
                    }
                }
            ]
        return None
