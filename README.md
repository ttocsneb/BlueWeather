# BlueWeather

[![tb]][Trello]
[![docsb]][docs]
[![Build Master]][bd]
[![Grade Master]][gm]

> This software is still in early development.

| Branch   | Build                 | Docs               | Grade                 |
|----------|-----------------------|--------------------|-----------------------|
| [Master] | [![Build Master]][bd] | [![docsbm]][docsm] | [![Grade Master]][gm] |
| [Devel]  | [![Build Devel]][bd]  | [![docsbd]][docsd] | [![Grade Devel]][gp]  |

BlueWeather is an open-source personal weather station (PWS) web-app. It
connects your weather station hardware to a website allowing you to view
your weather from your phone or computer.

## Spec

I originally started this project for my dad who's weather station broke. I
wanted to re-purpose the working hardware into a smart weather station that he
could access from his phone. Possibly even view from the internet.

BlueWeather has become such a big project for me. I have worked on it for over
2 years now; making large changes to core of the project, as well as
feature-creep further delaying anything useful from coming to fruition. I want
to stop this, and decide what the app will look like once and for all! From now
on, I will not make any large changes to the design of the app, and any
additions I want to add may only be done after The app is functional.

---

### Framework

BlueWeather will operate using python + django as a back-end and Bootstrap + Vue
as a front-end. To serve Vue, NPM will be used.

> I don't know a whole lot about NPM, but I hope that I will be able to use
> .vue files for the front-end, and compile them into individual js scripts
> without bundling. This may not be possible, but we will see.

### Apps

There will be several apps that help manage blueweather. This includes viewing
the weather, managing settings, managing accounts, and managing plugins.

#### Weather

This app will display the weather.

#### Accounts

This app will serve the login/register pages as well as the accounts, and
general admin page.

#### Settings

This app will serve all the application settings, as well as all of the
plugins settings.

---

### Plugins

There is no way this app could be useful without the integration of plugins.
Plugins will allow for the ability to interact with hardware, as well as
provide ways to process data in ways I could never do on my own.

I plan to use Stevedore to manage plugins. Plugins will register with the app
to have different types of services, such as a hardware interface, data
processing, django sub-app, and possibly more I haven't yet thought of.

> From what I have gathered, Stevedore uses the built-in setuptools library to
> collect plugins.

### Command Line Interface

The CLI will be able to manage plugins, settings, django, and starting the
application

> I hope to integrate the cli with django's manage.py to make managing the app
> more seamless.

### API

> Not much is known about how the API will act yet

This app will of course support a ReST API allowing for external integration
with things such as Android/iOS/desktop apps.

<!-- Badge Links -->

[Build Master]: https://github.drone.home.benscraft.info/api/badges/ttocsneb/BlueWeather/status.svg?ref=refs/heads/master
[Build Devel]: https://github.drone.home.benscraft.info/api/badges/ttocsneb/BlueWeather/status.svg?ref=refs/heads/devel
[bd]: https://github.drone.home.benscraft.info/ttocsneb/BlueWeather

[Grade Master]: https://www.codefactor.io/repository/github/ttocsneb/blueweather/badge
[gm]: https://www.codefactor.io/repository/github/ttocsneb/blueweather

[Grade devel]: https://www.codefactor.io/repository/github/ttocsneb/blueweather/badge/devel
[gp]: https://www.codefactor.io/repository/github/ttocsneb/blueweather/overview/devel

[Master]: https://github.com/ttocsneb/BlueWeather/
[Devel]: https://github.com/ttocsneb/BlueWeather/tree/devel

[Trello]: https://trello.com/b/fhguq1j3/blueweather
[tb]: https://img.shields.io/badge/Trello-View-blue

[docsb]: https://img.shields.io/readthedocs/blueweather
[docsbd]: https://img.shields.io/readthedocs/blueweather/devel
[docsbm]: https://img.shields.io/readthedocs/blueweather/master
[docs]: https://blueweather.readthedocs.io
[docsd]: https://blueweather.readthedocs.io/en/devel
[docsm]: https://blueweather.readthedocs.io/en/master
