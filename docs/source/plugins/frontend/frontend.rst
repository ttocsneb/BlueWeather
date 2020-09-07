FrontEnd
========

The front-end is built with Vue.js. It is a very powerful engine. This allows
the webpage to change or update seamlessly without having to reload the page.

.. toctree::

    settings

TypeScript
----------

I really like TypeScript, so I have added support for compiling typescript
into javascript.

Compiling TypeScript
^^^^^^^^^^^^^^^^^^^^

At the moment, there is no standardization for anything involving npm. So for
the moment, custom npm packages will need to be added manually, and compiling
to typescript must be done from your own npm installation, or using the
provided one.

In the future, I will come up with a proper solution for integrating npm and
typescript.

If you are wanting to use the types provided by BlueWeather, it will be easiest
to develop your plugins in a subdirectory of BlueWeather. It is not ideal, but
that is what we have for now.

You can then call :code:`npx tsc` to compile all ts files. The output will be
in the same directory as your source.