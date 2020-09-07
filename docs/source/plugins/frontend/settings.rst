Settings Frontend
=================

The frontend for the settings is very interesting. It is built using a single
Vue App integrating with all of the settings extensions components.

To be able to load your setting's component, you must register your component
globally, and supply the name of your component in the extension. (This is
not yet implemented, but is very important)

API
---

.. note::

    These API definitions aren't actual python classes, but instead
    representations of how the js components should act.

.. class:: frontend.settings.SettingsComponent

    This is the main component for displaying your settings.

    :param config: The config data for your component

    :usage:

        .. code-block:: js

            Vue.component('settings-component-name', {
                props: {
                    config: Object
                },
                template: '<a>Your Template Here</a>'
            });

    .. function:: popup(component: string, title: string: payload: any)

        Create a popup modal

        :param component: The name of the popup component
        :param title: The title of the popup
        :param payload: any object to send to the component

        .. note:: 

            If you need to be able to send data back to your original component, you can
            add functions to the payload.

        :usage:

            .. code-block:: js

                this.$emit('popup', {
                    component: 'component-name',
                    title: 'title',
                    payload: 'any object'
                }

.. class:: frontend.settings.PopupComponent

    This is the component used for managing the popup modal.

    :param payload: The data sent to the component from the :meth:`~frontend.settings.SettingsComponent.popup` event

    :usage:

        .. code-block:: js

            Vue.component('component-name', {
                props: {
                    payload: Object
                },
                template:
                '<div>' +
                    '<div class="modal-body">' +
                    '</div>' + 
                    '<div class="modal-footer">' + 
                    '</div>' +
                '</div>'
            });
    
    .. function:: close()

        Close the popup.

        :usage:

            .. code-block:: js

                this.$emit('close')