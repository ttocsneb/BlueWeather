import os

import flask
import flask_login

from blueweather import variables

_weather = 'clear'

def setWeatherIcon(weather: str):
    global _weather
    _weather = weather

def get_bread_crumb(url: str):
    if url == variables.config.web.home_page:
        return [
            {
                'name': os.path.basename(url).title()
            }
        ]

    breadcrumb = list()

    breadcrumb.append({
        'name': os.path.basename(variables.config.web.home_page).title(),
        'url': variables.config.web.home_page
    })

    middle, end = os.path.split(url)

    for part in middle.split('/'):
        if part == '':
            continue
        breadcrumb.append({
            'name': part.title(),
            'url': middle[:middle.index(part) + len(part)]
        })

    breadcrumb.append({
        'name': end.title()
    })

    return breadcrumb


def get_weather_icon(weather: str) -> str:
    """
    Get the ``weather-icons`` icon for the current weather. the options are

    ``clear, fog, rain, sleet, snow-wind, thunderstorm, cloudy-high, cloudy,
    hail, rain-mix, sleet-storm, sprinkle, windy, cloudy-gusts,
    haze, rain-wind, snow, storm-showers, cloudy-windy, lightning, showers,
    snow-thunderstorm, partly-cloudy``
    """
    from datetime import datetime

    hour = datetime.now().hour

    if hour > 20 or hour < 7:
        # It's the night time
        specials = {
            'clear': 'wi wi-fw wi-night-clear',
            'fog': 'wi wi-fw wi-night-fog',
            'windy': 'wi wi-fw wi-windy',
        }
        if weather in specials:
            return specials[weather]

        return 'wi wi-fw wi-night-alt-{}'.format(weather)

    specials = {
        'clear': 'wi wi-fw wi-day-sunny',
        'partly-cloudy': 'wi wi-fw wi-day-sunny-overcast'
    }
    if weather in specials:
        return specials[weather]

    return 'wi wi-fw wi-day-{}'.format(weather)

current = 0

def get_side_bar(route: str):

    # In the future, I would like to more dynamically generate the sidebar data

    # base
    sidebar = [
        {
            'name': 'Dashboard',
            'icon': 'fas fa-fw fa-tachometer-alt',
            'url': flask.url_for('main.dashboard'),
            'active': route == 'main.dashboard'
        },
        {
            'name': 'Weather',
            'icon': get_weather_icon(_weather),
            'url': flask.url_for('main.data'),
            'active': route == 'main.data'
        }
    ]

    # Login required items
    if flask_login.current_user.is_authenticated:
        sidebar.append('divider')

        # settings
        sidebar.append({
            'name': 'Settings',
            'icon': 'fas fa-cogs',
            'url': flask.url_for('main.config'),
            'active': route == 'main.config'
        })

    return sidebar

def get_web_variables(route_name: str, title=None) -> dict:
    args = dict()

    args['breadcrumbs'] = get_bread_crumb(flask.url_for(route_name))
    args['sidebar'] = get_side_bar(route_name)
    if title:
        args['title'] = title

    return args
