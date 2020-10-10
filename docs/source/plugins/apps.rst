Apps
====

Settings
--------

.. automodule:: blueweather.plugins.apps.config
    :members:


API
---

To use the api endpoint :code:`api/[app]/`, you need to register an api module
with the :code:`urlpatterns` variable. You can follow
`Django's Tutorial on urlpatterns <https://docs.djangoproject.com/en/3.1/ref/urls/>`_
for more information on creating your own url patterns.

To register the url patterns, you need to add the variable :code:`api` to your apps `AppConfig <https://docs.djangoproject.com/en/3.1/ref/applications/>`_.
The variable should contain the module name of yoru api url patterns:

app/apps.py:

.. code-block:: python

    class config(AppConfig):
        api = 'app.api'


app/api.py

.. code-block:: python

    from django.urls import path

    from . import views

    urlpatterns = [
        path('api_method', views.api_view, 'api_method')
    ]
