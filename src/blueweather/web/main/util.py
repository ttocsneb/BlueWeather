import os

from blueweather import variables

import flask
import flask_login

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
            'icon': 'wi wi-day-sunny fa-fw',
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
