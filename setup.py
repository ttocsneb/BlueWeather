from os import path
from setuptools import setup, find_packages


def description():
    description_file = path.join(
        path.abspath(path.dirname(__file__)),
        "README.md"
    )
    with open(description_file, encoding='utf-8') as f:
        return f.read()


INSTALL_REQUIRES = [
    'django>=3.0.7',
    'django-htmlmin>=0.11.0',
    'django-dresta@https://github.com/ttocsneb/django-dresta/archive/master.zip',
    'Jinja2>=2.11.1',
    'ruamel.yaml>=0.16.10',
    'marshmallow>=3.9.1',
    'markdown2>=2.3.9',
    'stringlike>=0.3.3',
    "importlib-metadata>=3.1.1 ; python_version<'3.8'"
]


setup(
    name="BlueWeather",
    version='0.5.0-alpha',

    description="A web-app for your Personal Weather Staion",
    long_description=description(),
    long_description_content_type="text/markdown",

    install_requires=INSTALL_REQUIRES,

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
    license='GPLv3',

    author='Benjamin Jacobs',
    author_email='benjammin1100@gmail.com',
    url='https://github.com/ttocsneb/BlueWeather',

    test_suite="testing.suite",

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
