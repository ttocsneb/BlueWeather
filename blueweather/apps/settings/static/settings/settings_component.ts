/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />
/// <reference types="settings" />

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

Vue.component('web-apikey-view', {
    props: {
        payload: Object
    },
    data() {
        return {
            size: {
                x: 200,
                y: 200
            }
        }
    },
    computed: {
        qrimg() {
            return `https://api.qrserver.com/v1/create-qr-code/?size=${this.size.x}x${this.size.y}&data=${this.payload}`
        }
    },
    template: `<div>
    <div class="modal-body text-center">
        <h6 class="text-uppercase">{{ payload }}</h6>
        <img :src="qrimg" width="size.x" height="size.y"></img>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Done</button>
    </div>
</div>`
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
            this.$emit("close")
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
    data: function() {
        return {
            sidebar: {
                type: "item",
                value: ""
            }
        }
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
        update_data(data: ApplyResponse) {
            if(data.success === true) {
                if("api_keys" in data.settings) {
                    this.config.api_keys = data.settings.api_keys
                }
                if("sidebar" in data.settings) {
                    this.config.sidebar = data.settings.sidebar
                }
            }
        },
        view_apikey(name: string) {
            let key: APIKey = this.config.api_keys.find((el: APIKey) => el.name == name )
            this.$emit('popup', {
                component: "web-apikey-view",
                title: name,
                payload: key.key
            })
        },
        delete_apikey(name: string) {
            this.$emit('popup', {
                component: "web-apikey-delete",
                title: 'Delete API Key',
                payload: {
                    name: name,
                    delete: this.on_delete_apikey
                }
            })
        },
        create_apikey() {
            console.log("Create API KEY")
            this.$emit('popup', {
                component: "web-apikey-create",
                title: 'Create API Key',
                payload: {
                    create: this.on_create_apikey,
                    keys: this.config.api_keys
                }
            })
        },
        update_api() {
            let settings: UpdateSettings = {
                namespace:"web",
                data: {
                    "api_keys": this.config.api_keys
                },
                success: this.update_data,
                error(jqXHR: JQueryXHR, textStatus: string, errorThrown: string) {
                    alert(`An error occurred: ${errorThrown}`)
                }
            }
            update_settings(settings)
        },
        on_delete_apikey(name: string) {
            console.log(`Going to delete ${name} key`)
            const key = this.config.api_keys.findIndex((el: APIKey) => el.name == name )
            this.$delete(this.config.api_keys, key)
            this.update_api()
        },
        on_create_apikey(name: string, permissions: Array<string>) {
            console.log(`Going to create ${name} key`)
            this.config.api_keys.push({
                name: name,
                permissions: permissions
            })
            this.update_api()
        },
        update_sidebar() {
            let settings: UpdateSettings = {
                namespace:"web",
                data: {
                    "sidebar": this.config.sidebar
                },
                success: this.update_data,
                error(jqXHR: JQueryXHR, textStatus: string, errorThrown: string) {
                    alert(`An error occurred: ${errorThrown}`)
                }
            }
            update_settings(settings)
        },
        sidebar_down(i: number) {
            let temp1 = this.config.sidebar[i]
            let temp2 = this.config.sidebar[i + 1]
            Vue.set(this.config.sidebar, i, temp2)
            Vue.set(this.config.sidebar, i + 1, temp1)
            this.update_sidebar()
        },
        sidebar_up(i: number) {
            let temp1 = this.config.sidebar[i]
            let temp2 = this.config.sidebar[i - 1]
            Vue.set(this.config.sidebar, i, temp2)
            Vue.set(this.config.sidebar, i - 1, temp1)
            this.update_sidebar()
        },
        sidebar_del(i: number) {
            Vue.delete(this.config.sidebar, i)
            this.update_sidebar()
        },
        sidebar_new() {
            let obj: SidebarItem = {
                category: this.sidebar.type,
            }
            if(obj.category == "item") {
                obj.value = this.sidebar.value
            }
            this.config.sidebar.push(obj)
            this.update_sidebar()
        }
    },
    template: `
<form action="#">
    <div class="form-group">
        <h4>API Keys</h4>
        <div class="table-responsive">
            <table class="table table-striped">
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
                        <td class="pr-2">
                            <button type="button" class="btn btn-link text-uppercase" @click="view_apikey(key.name)">{{ key.key }}</button>
                        </td>
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
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th></th>
                        <th>Type</th>
                        <th>Value</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(el, i) in config.sidebar">
                        <td>
                            <button :disabled="i == config.sidebar.length - 1" @click="sidebar_down(i)" type="button" class="btn btn-sm btn-link">
                                <i class="fas fa-level-down-alt"></i>
                            </button>
                            <button :disabled="i == 0" @click="sidebar_up(i)" type="button" class="btn btn-sm btn-link">
                                <i class="fas fa-level-up-alt"></i>
                            </button>
                        </td>
                        <td>{{ el.category }}</td>
                        <td>{{ el.value }}</td>
                        <td>
                            <button type="button" @click="sidebar_del(i)" class="btn btn-sm btn-danger">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>
                            <select class="form-control" v-model="sidebar.type">
                                <option>item</option>
                                <option>divider</option>
                            </select>
                        </td>
                        <td>
                            <input type="text" class="form-control" :disabled="sidebar.type == 'divider'" v-model="sidebar.value" placeholder="Value"/>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary" @click="sidebar_new">
                                <i class="fas fa-plus"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</form>
`
})