/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />

interface APIKey {
    name: string
    key: string
    permissions: Array<string>
}

Vue.component('settings-component', {
    props: {
        config: Object
    },
    beforeMount: function() {
        console.log(this.config)
    },
    template: `
<p>Settings</p>
`
})

Vue.component('web-apikey-create', {
    props: {
        payload: Object
    },
    data: function() {
        return {
            name: '',
            permissions: []
        }
    },
    methods: {
        create: function() {
            this.payload.create(this.name, this.permissions)
            this.$emit("close")
            this.name = ''
            this.permissions = []
        },
        findKey: function(name: string) {
            return this.payload.keys.find((el: APIKey) => el.name == name)
        }
    },
    computed: {
        valid: function() {
            if(this.findKey(this.name) != null) {
                return false
            }
            return this.name.length > 0
        },
        message: function() {
            if(this.findKey(this.name) != null) {
                return "A key with that name already exists"
            }
            if(this.name.length == 0) {
                return "This is required"
            }
            return ""
        }
    },
    template: `<div>
    <div class="modal-body">
        <p>Create a new API Key</p>
        <form @submit="create" action="#">
            <div class="form-group">
                <input type="text" class="form-control" :class="{'is-invalid': !valid}" v-model.trim="name" placeholder="Name" />
                <div v-if="message" class="invalid-feedback">
                    {{ message }}
                </div>
            </div>
        </form>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-primary" :disabled="!valid" data-dismiss="modal" @click="create">Create</button>
    </div>
</div>`
})

Vue.component('web-apikey-delete', {
    props: {
        payload: Object
    },
    methods: {
        remove: function() {
            this.payload.delete(this.payload.name)
        }
    },
    template: `<div>
    <div class="modal-body">
        <p>
            Are you sure you want to delete the API Key <code>{{ payload.name }}</code>?
        </p>
        <p>
            This action is irriversable and will stop any devices using this
            key from accessing your server.
        </p>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-danger" data-dismiss="modal" @click="remove">Delete</button>
    </div>
</div>`
})

Vue.component('web-settings-component', {
    props: {
        config: Object
    },
    beforeMount: function() {
        console.log(this.config)
        console.log(this.settings)
    },
    computed: {
        settings: function() {
            return JSON.stringify(this.config, null, 2)
        }
    },
    methods: {
        delete_apikey: function(name: string) {
            this.$emit('popup', {
                component: "web-apikey-delete",
                title: 'Delete API Key',
                payload: {
                    name: name,
                    delete: this.on_delete_apikey
                }
            })
        },
        create_apikey: function() {
            console.log("Create API KEY")
            this.$emit('popup', {
                component: "web-apikey-create",
                title: 'Create API Key',
                payload: {
                    create: this.on_create_apikey,
                    keys: this.config.api_keys
                }
            })
            // TODO Create a web-apikey-create component
        },
        on_delete_apikey: function(name: string) {
            console.log(`Going to delete ${name} key`)
            const key = this.config.api_keys.findIndex((el: APIKey) => el.name == name )
            this.$delete(this.config.api_keys, key)
            // TODO Actually send the message to the server
        },
        on_create_apikey: function(name: string, permissions: Array<string>) {
            console.log(`Going to create ${name} key`)
            this.config.api_keys.push({
                name: name,
                key: "AAAAAAAAAAAAAA",
                permissions: permissions
            })
            // TODO Actually send the message to the server
        }
    },
    template: `
<form>
    <div class="form-group">
        <h4>API Keys</h4>
        <div class="table-responsive">
            <table class="table table-striped width">
                <thead>
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Key</th>
                        <th class="pr-2" scope="col">Permissions</th>
                        <th class="py-1" scope="col">
                            <button type="button" @click="create_apikey" class="btn btn-primary">Create</button>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="key in config.api_keys">
                        <th class="px-2" scope="row">{{ key.name }}</th>
                        <td class="pr-2 text-uppercase">{{ key.key }}</td>
                        <td class="pr-2">
                            <ul v-if="key.permissions && key.permissions.length">
                                <li v-for="i in key.permissions">
                                    {{ i }}
                                </li>
                            </ul>
                            <span v-else>
                                None
                            </span>
                        </td>
                        <td class="pr-2 py-1">
                            <button type="button" @click="delete_apikey(key.name)" class="btn btn-danger">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p class="mt-2">
            Each Key has permissions associated with them, that way, you can
            allow those you don't trust to get access to the server without
            comprimising security.
        </p>
    </div>
    <hr>
    <div class="form-group">
        <h4>Sidebar</h4>
    </div>
</form>
`
})