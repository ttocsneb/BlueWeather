Blueweather Structure
=====================

The Blueweather project is a rather large project, and so needs to have a
solid plan to make it work. This page is where you can find the plan.

ReST API
========

I have thought about ways that the rest api can be structured. I think that I
want the api to be accessible by anyone who has access to it. The api will
always use json objects. The api functions will be separated from django's
view system. This will allow for more focus on the api.

My thought is to have all the api calls be defined in a :code:`api` module.
Each function will use an api decorator that creates an api class. This class
will be able to read the signature of the api function and extract the
required parameters. You can also give options for how the api should act.

You can also supply a marshmallow model that can create a schema that will
tell clients what to expect.


Client Side Vs Server Side
==========================

I want the client side to be disconnected from the server side. This will
allow for different client-side apps to be easily created without worrying
about what the front-end wants.

Because I want the front-end to be separated from the back-end, I will have a
separate app that can be configured to serve the front-end. This way, someone
else could create their own front-end to use instead.

Plugins
=======

I have tried using stevedore in the past for plugins. It seems to work very
well, but I realized that it doesn't make much sense to use it when django has
their own plugin system already built.