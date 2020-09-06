Vue.component('settings-component', {
    props: {
        config: Object
    },
    beforeMount: function () {
        console.log(this.config);
    },
    template: "\n<p>Settings</p>\n"
});
Vue.component('web-apikey-create', {
    props: {
        payload: Object
    },
    data: function () {
        return {
            name: '',
            permissions: []
        };
    },
    methods: {
        create: function () {
            this.payload.create(this.name, this.permissions);
            this.$emit("close");
            this.name = '';
            this.permissions = [];
        },
        findKey: function (name) {
            return this.payload.keys.find(function (el) { return el.name == name; });
        }
    },
    computed: {
        valid: function () {
            if (this.findKey(this.name) != null) {
                return false;
            }
            return this.name.length > 0;
        },
        message: function () {
            if (this.findKey(this.name) != null) {
                return "A key with that name already exists";
            }
            if (this.name.length == 0) {
                return "This is required";
            }
            return "";
        }
    },
    template: "<div>\n    <div class=\"modal-body\">\n        <p>Create a new API Key</p>\n        <form @submit=\"create\" action=\"#\">\n            <div class=\"form-group\">\n                <input type=\"text\" class=\"form-control\" :class=\"{'is-invalid': !valid}\" v-model.trim=\"name\" placeholder=\"Name\" />\n                <div v-if=\"message\" class=\"invalid-feedback\">\n                    {{ message }}\n                </div>\n            </div>\n        </form>\n    </div>\n    <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Cancel</button>\n        <button type=\"button\" class=\"btn btn-primary\" :disabled=\"!valid\" data-dismiss=\"modal\" @click=\"create\">Create</button>\n    </div>\n</div>"
});
Vue.component('web-apikey-delete', {
    props: {
        payload: Object
    },
    methods: {
        remove: function () {
            this.payload.delete(this.payload.name);
        }
    },
    template: "<div>\n    <div class=\"modal-body\">\n        <p>\n            Are you sure you want to delete the API Key <code>{{ payload.name }}</code>?\n        </p>\n        <p>\n            This action is irriversable and will stop any devices using this\n            key from accessing your server.\n        </p>\n    </div>\n    <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Cancel</button>\n        <button type=\"button\" class=\"btn btn-danger\" data-dismiss=\"modal\" @click=\"remove\">Delete</button>\n    </div>\n</div>"
});
Vue.component('web-settings-component', {
    props: {
        config: Object
    },
    beforeMount: function () {
        console.log(this.config);
        console.log(this.settings);
    },
    computed: {
        settings: function () {
            return JSON.stringify(this.config, null, 2);
        }
    },
    methods: {
        delete_apikey: function (name) {
            this.$emit('popup', {
                component: "web-apikey-delete",
                title: 'Delete API Key',
                payload: {
                    name: name,
                    delete: this.on_delete_apikey
                }
            });
        },
        create_apikey: function () {
            console.log("Create API KEY");
            this.$emit('popup', {
                component: "web-apikey-create",
                title: 'Create API Key',
                payload: {
                    create: this.on_create_apikey,
                    keys: this.config.api_keys
                }
            });
        },
        on_delete_apikey: function (name) {
            console.log("Going to delete " + name + " key");
            var key = this.config.api_keys.findIndex(function (el) { return el.name == name; });
            this.$delete(this.config.api_keys, key);
        },
        on_create_apikey: function (name, permissions) {
            console.log("Going to create " + name + " key");
            this.config.api_keys.push({
                name: name,
                key: "AAAAAAAAAAAAAA",
                permissions: permissions
            });
        }
    },
    template: "\n<form>\n    <div class=\"form-group\">\n        <h4>API Keys</h4>\n        <div class=\"table-responsive\">\n            <table class=\"table table-striped width\">\n                <thead>\n                    <tr>\n                        <th scope=\"col\">Name</th>\n                        <th scope=\"col\">Key</th>\n                        <th class=\"pr-2\" scope=\"col\">Permissions</th>\n                        <th class=\"py-1\" scope=\"col\">\n                            <button type=\"button\" @click=\"create_apikey\" class=\"btn btn-primary\">Create</button>\n                        </th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr v-for=\"key in config.api_keys\">\n                        <th class=\"px-2\" scope=\"row\">{{ key.name }}</th>\n                        <td class=\"pr-2 text-uppercase\">{{ key.key }}</td>\n                        <td class=\"pr-2\">\n                            <ul v-if=\"key.permissions && key.permissions.length\">\n                                <li v-for=\"i in key.permissions\">\n                                    {{ i }}\n                                </li>\n                            </ul>\n                            <span v-else>\n                                None\n                            </span>\n                        </td>\n                        <td class=\"pr-2 py-1\">\n                            <button type=\"button\" @click=\"delete_apikey(key.name)\" class=\"btn btn-danger\">Delete</button>\n                        </td>\n                    </tr>\n                </tbody>\n            </table>\n        </div>\n        <p class=\"mt-2\">\n            Each Key has permissions associated with them, that way, you can\n            allow those you don't trust to get access to the server without\n            comprimising security.\n        </p>\n    </div>\n    <hr>\n    <div class=\"form-group\">\n        <h4>Sidebar</h4>\n    </div>\n</form>\n"
});
