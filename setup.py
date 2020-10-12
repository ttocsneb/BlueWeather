import os
from os import path
from setuptools import setup, find_packages


def description():
    description_file = path.join(
        path.abspath(path.dirname(__file__)),
        "README.md"
    )
    with open(description_file, encoding='utf-8') as f:
        return f.read()


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
    'django==3.0.7',
    'django-npm==1.0.0',
    'django-htmlmin==0.11.0',
    'Jinja2==2.11.1',
    'ruamel.yaml==0.16.10',
    'marshmallow==3.5.1',
    'stevedore==1.32.0',
    'markdown2==2.3.9'
]

EXTRAS_REQUIRE = {}

setup(
    name="BlueWeather",
    version='0.4.1-alpha',

    description="A web-app for your Personal Weather Staion",
    long_description=description(),
    long_description_content_type="text/markdown",

    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],

    author='Benjamin Jacobs',
    author_email='benjammin1100@gmail.com',
    url='https://github.com/ttocsneb/BlueWeather',

    test_suite="testing.suite",

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'blueweather.plugins.unitconv': [
            'imperialConverter = blueweather.plugins.integrated.converters:ImperialConversion',
            'metricConverter = blueweather.plugins.integrated.converters:MetricConversion'
        ],
        'blueweather.plugins.weather': [
            'dummyWeather = blueweather.plugins.integrated.dummyWeather:DummyWeather'
        ]
    }
)
