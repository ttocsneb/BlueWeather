Accounts
========

Manages the Accounts Page using :code:`auth` middleware from django.

AccountsConfig
--------------

.. autoclass:: blueweather.apps.accounts.apps.AccountsConfig
    :members:

    .. autoattribute:: AccountsConfig.name
    .. autoattribute:: AccountsConfig.label
    .. autoattribute:: AccountsConfig.verbose_name
    .. autoattribute:: AccountsConfig.icon

.. currentmodule:: blueweather.apps.accounts

URLS
----

.. class:: blueweather.apps.accounts.urls.urlpatterns

    .. attribute:: login

        :endpoint: `login/`
        :view: :code:`auth_views.LoginView`

    .. attribute:: logout

        :endpoint: `logout/`
        :view: :code:`auth_views.LogoutView`
    
    .. attribute:: password_change

        :endpoint: `password_change/`
        :view: :code:`auth_views.PasswordChaneView`

    .. attribute:: password_change_done

        :endpoint: `password_change/done/`
        :view: :code:`auth_views.PasswordChangeDoneView`

    .. attribute:: profile

        :endpoint: `profile/`
        :view: :meth:`views.profile`
    
    .. attribute:: default

        :endpoint: `/`
        :view: :meth:`views.index`

Views
--------

.. automodule:: blueweather.apps.accounts.views
    :members: