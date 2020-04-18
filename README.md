# BlueWeather

> This software is still in early development.

| Branch   | Build | Grade | Progress | Lines |
|----------|-------|-------|----------|-------|
| [Master] | [![Build Master]][bd] | [![Grade Master]][gm] | [![Progress Master]][Master] | [![Lines Master]][Master] |
| [Django] | [![Build Django]][bd] | [![Grade Django]][gd] | [![Progress Django]][Django] | [![Lines Django]][Jdango] |

> Progress comes from the number of checked check boxes in this readme. The
> Progress may not be accurate as I do not yet have the TODOs set in stone

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

### TODO

* [ ] [Build Framework](#Framework)
* [ ] [Build Plugin Manager](#Plugins)
* [ ] [Build CLI](#Command-Line-Interface)
* [ ] [Build API](#API)

---

### Framework

BlueWeather will operate using python + django as a back-end and Bootstrap + Vue
as a front-end. To serve Vue, NPM will be used.

> I don't know a whole lot about NPM, but I hope that I will be able to use
> .vue files for the front-end, and compile them into individual js scripts
> without bundling. This may not be possible, but we will see.

#### Framework TODO

* [X] Setup Django Framework
  * [ ] Setup Plugin Django Apps
* [X] Setup NPM
* [ ] Setup Vue

### Plugins

There is no way this app could be useful without the integration of plugins.
Plugins will allow for the ability to interact with hardware, as well as
provide ways to process data in ways I could never do on my own.

I plan to use Stevedore to manage plugins. Plugins will register with the app
to have different types of services, such as a hardware interface, data
processing, django sub-app, and possibly more I haven't yet thought of.

> From what I have gathered, Stevedore uses the built-in setuptools library to
> collect plugins.

#### Plugin TODO

* [ ] Setup Stevedore
* [ ] Collect Plugins
* [ ] Create Plugin Management App
  * [ ] Download and install plugins
* [ ] Create Integrated Plugins (_Plugins that are built in to BlueWeather that
use extensions_)

### Command Line Interface

The CLI will be able to manage plugins, settings, django, and starting the
application

> I hope to integrate the cli with django's manage.py to make managing the app
> more seamless.

#### CLI TODO

* [ ] Integrate CLI options with manage.py
* [ ] Add Plugin Commands
* [ ] Add Setting Commands
* [ ] Add Start Command

### API

> Not much is known about how the API will act yet

This app will of course support a ReST API allowing for external integration
with things such as Android/iOS/desktop apps.

#### API TODO

* [ ] Create API App
* _Plan more for the API_

<!-- Badge Links -->

[Build Master]: https://github.drone.home.benscraft.info/api/badges/ttocsneb/BlueWeather/status.svg?ref=refs/heads/master
[Build Django]: https://github.drone.home.benscraft.info/api/badges/ttocsneb/BlueWeather/status.svg?ref=refs/heads/django
[bd]: https://github.drone.home.benscraft.info/ttocsneb/BlueWeather

[Grade Master]: https://www.codefactor.io/repository/github/ttocsneb/blueweather/badge
[gm]: https://www.codefactor.io/repository/github/ttocsneb/blueweather

[Grade Django]: https://www.codefactor.io/repository/github/ttocsneb/blueweather/badge/django
[gd]: https://www.codefactor.io/repository/github/ttocsneb/blueweather/overview/django

[Progress Master]: ../master/badges/progress.svg
[Progress Django]: ../django/badges/progress.svg

[Lines Master]: ../master/badges/lines.svg
[Lines Django]: ../django/badges/lines.svg

[Master]: https://github.com/ttocsneb/BlueWeather/
[Django]: https://github.com/ttocsneb/BlueWeather/tree/django

