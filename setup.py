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
    'django==3.0.5',
    'django-npm==1.0.0',
    'django-htmlmin==0.11.0',
    'Jinja2==2.11.1',
    'ruamel.yaml==0.16.10',
    'marshmallow==3.5.1',
    'stevedore'
]

EXTRAS_REQUIRE = {}

setup(
    name="BlueWeather",
    version='0.2.0',

    description="A web-app for your Personal Weather Staion",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,

    classifiers=[
        "Development Status :: 1 - Planning",
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
            'imperial = blueweather.plugins.integrated.imperialConv:ImperialConversion',
            'metric = blueweather.plugins.integrated.imperialConv:MetricConversion'
        ],
        'blueweather.plugins.weather': [
            'dummyWeather = blueweather.plugins.integrated.dummyWeather:DummyWeather'
        ]
    }
)
