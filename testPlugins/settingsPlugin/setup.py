import os
from setuptools import setup, find_packages

setup(
    name="DummySettingsPlugin",
    version='0.0.1',
    
    entry_points={
        'blueweather.plugins.plugin': [
            'dummySettings = settingsPlugin:DummySettings'
        ],
        'blueweather.plugins.settings': [
            'dummySettings = settingsPlugin:DummySettings'
        ]
    }
)
