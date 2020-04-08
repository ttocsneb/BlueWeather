from django.apps import AppConfig


class WeatherConfig(AppConfig):
    label = 'blueweather.weather'
    name = 'blueweather.weather'
    route = 'weather:index'
    verbose_name = 'Weather'
    icon = 'wi wi-day-cloudy'
