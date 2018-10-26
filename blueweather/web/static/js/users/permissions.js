
new Vue({
    el: '#permissions-edit-users',
    data: {
        userData: [],
        editorData: {}
    },
    beforeCreate: function() {
        // Load the privilege data from the server
        $.get("/users/privileges/get").done(data => {
            console.log("got privilege data");
            this.editorData = data.editor;
            this.userData = data.perm;
        });
    },
    components: {
        'perm-user': {
            data: function() {
                return {
                    form: {
                        add_user: false,
                        change_perm: false,
                        change_settings: false,
                        reboot: false,
                        id: 0
                    },
                    defaults: {
                        add_user: false,
                        change_perm: false,
                        change_settings: false,
                        reboot: false
                    },
                    disabled: {
                        disabled: false,
        
                        add_user: false,
                        change_perm: false,
                        change_settings: false,
                        reboot: false
                    },
                    alert: {
                        class: "",
                        alert: ""
                    },
                    button: {
                        class: "",
                        title: ""
                    },
                    enable: false
                };
            },
            props: {
                user: Object,
                editor: Object
            },
            created: function() {
                

                // Set defaults
                this.defaults.add_user = this.user.add_user;
                this.defaults.change_perm = this.user.change_perm;
                this.defaults.change_settings = this.user.change_settings;
                this.defaults.reboot = this.user.reboot;

                // Set current values
                this.form.id = this.user.id;
                this.form.add_user = this.defaults.add_user;
                this.form.change_perm = this.defaults.change_perm;
                this.form.change_settings = this.defaults.change_settings;
                this.form.reboot = this.defaults.reboot;

        
                // Disable the editor if the user is the editor
                var disabled = this.user.id == this.editor.id
                this.disabled.disabled = disabled;
        
                // Set the disabled options
                this.disabled.add_user = !this.editor.add_user;
                this.disabled.change_perm = !this.editor.change_perm;
                this.disabled.change_settings = !this.editor.change_settings;
                this.disabled.reboot = !this.editor.reboot;
        
                // Set the Button values
                this.button.class = {
                    'btn-secondary': disabled,
                    nohover: disabled,
                    active: disabled,
                    'btn-outline-info': !disabled
                };

                // Set the title of the button to the username + (you) if the user is you
                this.button.title = this.user.name + (disabled ? " (you)" : "");
            },
            methods: {
                change: function() {
                    // Show the checkbox as active for bootstrap when the button is checked
                    Vue.set(this.button.class, "active", !this.enable);
                    
                    // Reset the alert
                    Vue.set(this.alert, 'class', '');
                    Vue.set(this.alert, 'alert', '');
                },
                submit: function() {
                    var request = $.ajax({
                        url: "/users/privileges/set",
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify(this.form)
                    });

                    request.done((data) => {
                        if(data == 'true') {
                            // on success
                            Vue.set(this.alert, "alert", "Successfully Changed Permissions!");
                            Vue.set(this.alert, "class", "alert-success");
        
                            Vue.set(this.defaults, "add_user", this.form.add_user);
                            Vue.set(this.defaults, "change_perm", this.form.change_perm);
                            Vue.set(this.defaults, "change_settings", this.form.change_settings);
                            Vue.set(this.defaults, "reboot", this.form.reboot);
                        } else {
                            // on fail
                            Vue.set(this.alert, "alert", data);
                            Vue.set(this.alert, "class", "alert-danger");
                        }
                    });

                    request.fail(() => {
                        // On Fail
                        Vue.set(this.alert, "alert", "Something went wrong while saving.");
                        Vue.set(this.alert, "class", "alert-warning");
                    });
                },
                cancel: function() {
                    // Set the form values to be the current values on the server
                    Vue.set(this.form, 'add_user', this.defaults.add_user);
                    Vue.set(this.form, 'change_perm', this.defaults.change_perm);
                    Vue.set(this.form, 'change_settings', this.defaults.change_settings);
                    Vue.set(this.form, 'reboot', this.defaults.reboot);
        
                    // Reset the alert
                    Vue.set(this.alert, 'class', '');
                    Vue.set(this.alert, 'alert', '');
                }
            },
            template: 
`<div>
    <div class="btn-group-toggle">
        <label class="btn" v-bind:class="button.class">
            <input type="checkbox" v-on:click="change" v-model="enable" v-bind:disabled="disabled.disabled"/>
            {{ button.title }}
        </label>
    </div>

    <div class="form-group" v-if="enable">
        <legend class="border-bottom mb-4 mt-3">Edit Permissions</legend>
        <div class="alert" v-bind:class="alert.class" v-if="alert.alert">{{ alert.alert }}</div>

        <div class="row mt-4">
            <div class="col-6"><div class="form-group ml-4">
                <div class="row"><label class="form-check-label">
                    <input type="checkbox" v-model="form.add_user" v-bind:disabled="disabled.add_user"/>
                    Create Users
                </label></div>
                <div class="row"><label class="form-check-label">
                    <input type="checkbox" v-model="form.change_perm" v-bind:disabled="disabled.change_perm"/>
                    Edit Permissions
                </label></div>
                <div class="row"><label class="form-check-label">
                    <input type="checkbox" v-model="form.change_settings" v-bind:disabled="disabled.change_settings"/>
                    Change Settings
                </label></div>
                <div class="row"><label class="form-check-label">
                    <input type="checkbox" v-model="form.reboot" v-bind:disabled="disabled.reboot"/>
                    Reboot
                </label></div>
            </div></div>

            <div class="col-4 mt-2">
                <div class="form-group">
                    <input type="button" class="btn btn-danger btn-sm" v-on:click="submit" value="Save"/>
                </div>
                <div class="form-group">
                    <input type="button" class="btn btn-warning btn-sm" v-on:click="cancel" value="Cancel"/>
                </div>
            </div>
        </div>
    </div>
</div>`
        }
    }
});
