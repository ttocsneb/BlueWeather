import os
from setuptools import setup, find_packages

setup(
    name="DummyStartupPlugin",
    version='0.0.1',
    
    entry_points={
        'blueweather.plugins.startup': [
            'dummyStartup = startupPlugin:DummyStartup'
        ],
        'blueweather.plugins.plugin': [
            'dummyStartup = startupPlugin:DummyStartup'
        ]
    }
)