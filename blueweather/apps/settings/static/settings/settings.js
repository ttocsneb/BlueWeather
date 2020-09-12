function validationToString(error, base) {
    if (base === void 0) { base = ""; }
    if (!Array.isArray(error)) {
        var groups = error;
        var messages = [];
        if (base != "") {
            base += ".";
        }
        for (var k in groups) {
            messages.push(validationToString(groups[k], "" + base + k));
        }
        return _.join(messages, "\n");
    }
    else {
        return base + ":\n - " + _.join(error, '\n - ');
    }
}
function update_settings(config) {
    $.ajax("/api/settings/apply/", {
        method: "POST",
        data: JSON.stringify({
            namespace: config.namespace,
            settings: config.data
        }),
        success: function (data, textStatus, jqXHR) {
            if (data.success == false && data.validation != null) {
                console.error(data.reason + ":\n" + validationToString(data.validation));
            }
            config.success(data, textStatus, jqXHR);
        },
        error: config.error
    });
}
function loadedComponents() {
    var loaded = [];
    var components = this.$options.components;
    for (var key in components) {
        loaded.push(key);
    }
    return loaded;
}
function componentExists(component) {
    var components = loadedComponents.call(this);
    if (components.indexOf(component) !== -1) {
        return true;
    }
    return false;
}
function checkComponent(self, component) {
    var value = componentExists.call(self, component);
    if (value == false) {
        console.error("The component '" + component + "' Does not exist!\nMaybe your settings are not configured correctly.");
    }
    return value;
}
var settings_component = Vue.extend({
    props: {
        title: String,
        child: String,
        config: String
    },
    data: function () {
        return {
            settings: JSON.parse(this.config)
        };
    },
    beforeMount: function () {
        checkComponent(this, this.child);
    },
    methods: {
        onPopup: function (popup) {
            this.$emit('popup', popup);
        },
        onChanged: function () {
            this.$emit('change');
        }
    },
    template: "\n<div class=\"card shadow mb-2\">\n    <div class=\"card-header\">{{ title }}</div>\n    <div class=\"card-body\">\n        <component :is=\"child\" :config=\"settings\" @popup=\"onPopup\" @change=\"onChanged\" />\n    </div>\n</div>\n"
});
var settings = new Vue({
    delimiters: ['[[', ']]'],
    el: '#settings',
    props: ['title'],
    components: {
        'settings-card': settings_component
    },
    data: function () {
        return {
            popup: {
                component: null,
                title: "Title",
                payload: {}
            },
            changed: modified
        };
    },
    computed: {
        save: function () {
            if (this.changed) {
                return "inline";
            }
            else {
                return "none";
            }
        }
    },
    methods: {
        onPopup: function (popup) {
            if (!checkComponent(this, popup.component)) {
                return;
            }
            this.popup.component = popup.component;
            if (popup.title != null) {
                this.popup.title = popup.title;
            }
            else {
                this.popup.title = "Popup";
            }
            if (popup.payload != null) {
                this.popup.payload = popup.payload;
            }
            else {
                this.popup.payload = null;
            }
            $("#settings-modal").modal();
        },
        close: function () {
            console.log("Closing Modal");
            $("#settings-modal").modal("hide");
        },
        onSave: function () {
            $.ajax("/api/settings/save/", {
                method: "POST",
                success: function (data, textStatus, jqXHR) {
                    console.log("Settings have been saved");
                    this.changed = false;
                },
                error: function () {
                    alert("The settings could not be saved :/");
                }
            });
        },
        onReset: function () {
            $.ajax("/api/settings/revert/", {
                method: "POST",
                success: function (data, textStatus, jqXHR) {
                    location.reload();
                },
                error: function () {
                    alert("The settings could not be reverted :/");
                }
            });
        },
        onChanged: function () {
            this.changed = true;
        }
    }
});
