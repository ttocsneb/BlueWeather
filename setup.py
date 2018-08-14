import os
from setuptools import setup, find_packages


with open("README.md", 'r') as fh:
    LONG_DESCRIPTION = fh.read()


def package_data_dirs(source, sub_folders):
    dirs = []

    for d in sub_folders:
        folder = os.path.join(source, d)
        if not os.path.exists(folder):
            continue

        for dirname, _, files in os.walk(folder):
            dirname = os.path.relpath(dirname, source)
            for f in files:
                dirs.append(os.path.join(dirname, f))

    return dirs


INSTALL_REQUIRES = [
    'Flask',
    'Flask-Bcrypt',
    'Flask-Login',
    'Flask-SQLAlchemy',
    'Flask-WTF',
    'Jinja2',
    'yapsy',
    'requests',
    'ruamel.yaml'
]


def params():
    name = "BlueWeather"
    version = '0.0.1'

    description = "A web application that allows you to interface with your " \
        + "weather station"
    long_description = LONG_DESCRIPTION
    long_description_content_type = "text/markdown"

    install_requires = INSTALL_REQUIRES

    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
    author = 'Benjamin Jacobs'
    author_email = 'benjammin1100@gmail.com'
    url = 'https://github.com/ttocsneb/BlueWeather'

    packages = find_packages(where='src')
    package_dir = {'': 'src'}
    package_data = {
        'blueweather': package_data_dirs('src/blueweather',
                                         ['static', 'templates'])
    }

    include_package_data = True
    zip_safe = False

    entry_points = {
        'console_scripts': [
            'blueweather = blueweather:main'
        ]
    }

    return locals()


setup(**params())
