from django.apps import AppConfig


class WeatherConfig(AppConfig):
    label = 'blueweather.apps.weather'
    name = 'blueweather.apps.weather'
    route = 'weather:index'
    verbose_name = 'Weather'
    icon = 'wi wi-day-cloudy'
