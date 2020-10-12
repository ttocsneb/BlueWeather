.. BlueWeather documentation master file, created by
   sphinx-quickstart on Tue Aug 25 21:02:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BlueWeather's documentation
=======================================

Here you will find all the documentation needed to create your own plugins, or
to add to BlueWeather's Codebase.

This project is still early in development, so most of its features are missing,
or half-baked. Please keep this in mind when reading this documentation.

BlueWeather is a python web-app built to manage and serve the weather from your
Personal Weather Station (PWS). It is highly extensible allowing for virtually
infinite possibilies to measure the weather. In this documentation, you will
learn how to develop your own weather driver, as well as create plugins that can
process weather data, or interact with the user.

There is also documentation of the internal workings of BlueWeather, mostly for
my own sanity.


Contents
--------

.. toctree::
   :maxdepth: 2

   plugins/index
   web/api
   internal/index


Installation
------------

To install BlueWeather, the first step is to download it, which you can do by

.. note::

   Required Software

   * Python 3.6
   * npm

.. code-block:: shell

   git clone https://github.com/ttocsneb/blueweather.git

Once you have the source downloaded, you can install it by running

.. code-block:: shell

   cd blueweather
   python -m pip install .
   npm i

To start the server

.. code-block:: shell

   python manage.py runserver

Contribute
----------

* Trello: `https://trello.com/b/fhguq1j3/blueweather <https://trello.com/b/fhguq1j3/blueweather>`_
* Issue Tracker: `github.com/ttocsneb/blueweather/issues <https://github.com/ttocsneb/blueweather/issues>`_
* Source Code: `github.com/ttocsneb/blueweather <https://github.com/ttocsneb/blueweather>`_

License
-------

The project is licensed under GNU General Public License v3.0