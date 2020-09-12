/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />
/// <reference types="bootstrap" />
/// <reference types="settings" />

declare var modified: boolean


interface Popup {
    component: string
    payload: object
    title: string
}

function validationToString(error: ValidationType, base: string = ""): string {
    if(!Array.isArray(error)) {
        const groups = error as ValidationObject
        let messages = []
        if(base != "") {
            base += "."
        }
        for(var k in groups) {
            messages.push(validationToString(groups[k], `${base}${k}`))
        }
        return _.join(messages, "\n")
    } else {
        return `${base}:\n - ${_.join(error, '\n - ')}`
    }
}

function update_settings(config: UpdateSettings) {
    $.ajax("/api/settings/apply/", {
        method: "POST",
        data: JSON.stringify({
            namespace: config.namespace,
            settings: config.data
        }),
        success(data: ApplyResponse, textStatus: string, jqXHR: JQueryXHR) {
            if(data.success == false && data.validation != null) {
                console.error(`${data.reason}:\n${validationToString(data.validation)}`)
            }
            config.success(data, textStatus, jqXHR)
        },
        error: config.error
    })
}

function loadedComponents(): Array<string> {
    var loaded = []
    const components = this.$options.components
    for (const key in components) {
        loaded.push(key)
    }
    return loaded
}

function componentExists(component: string): boolean {
    const components = loadedComponents.call(this);
    if(components.indexOf(component) !== -1) {
        return true
    }
    return false
}

function checkComponent(self: object, component: string): boolean {
    const value = componentExists.call(self, component)
    if(value == false) {
        console.error(`The component '${component}' Does not exist!
Maybe your settings are not configured correctly.`)
    }
    return value
}

const settings_component = Vue.extend({
    props: {
        title: String,
        child: String,
        config: String
    },
    data: function() {
        return {
            settings: JSON.parse(this.config)
        }
    },
    beforeMount: function() {
        checkComponent(this, this.child)
    },
    methods: {
        onPopup: function(popup: Popup) {
            this.$emit('popup', popup)
        },
        onChanged() {
            this.$emit('change')
        }
    },
    template: `
<div class="card shadow mb-2">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">
        <component :is="child" :config="settings" @popup="onPopup" @change="onChanged" />
    </div>
</div>
`
})

const settings = new Vue({
    delimiters: ['[[', ']]'],
    el: '#settings',
    props: ['title'],
    components: {
        'settings-card': settings_component
    },
    data: function() {
        return {
            popup: {
                component: null,
                title: "Title",
                payload: {}
            },
            changed: modified
        }
    },
    computed: {
        save() {
            if(this.changed) {
                return "inline"
            } else {
                return "none"
            }
        }
    },
    methods: {
        onPopup: function(popup: Popup) {
            if(!checkComponent(this, popup.component)) {
                return
            }
            this.popup.component = popup.component
            if(popup.title != null) {
                this.popup.title = popup.title
            } else {
                this.popup.title = "Popup"
            }
            if(popup.payload != null) {
                this.popup.payload = popup.payload
            } else {
                this.popup.payload = null
            }
            $("#settings-modal").modal()
        },
        close: function() {
            console.log("Closing Modal")
            $("#settings-modal").modal("hide")
        },
        onSave() {
            $.ajax("/api/settings/save/", {
                method: "POST",
                success(data: object, textStatus: string, jqXHR: JQueryXHR) {
                    console.log("Settings have been saved")
                    this.changed = false
                },
                error() {
                    alert("The settings could not be saved :/")
                }
            })
        },
        onReset() {
            $.ajax("/api/settings/revert/", {
                method: "POST",
                success(data: object, textStatus: string, jqXHR: JQueryXHR) {
                    location.reload()
                },
                error() {
                    alert("The settings could not be reverted :/")
                }
            })
        },
        onChanged() {
            this.changed = true
        }
    }
})