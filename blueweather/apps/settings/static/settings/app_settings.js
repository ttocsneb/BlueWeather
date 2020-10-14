var setting_value = Vue.extend({
    props: {
        name: String,
        settings: Array,
        value: {
            default: {},
            type: Object
        },
        app: String
    },
    methods: {
        on_input: function (event) {
            var target = event.target;
            var input = _.cloneDeep(this.value);
            var setting = this.setting;
            if (input == null) {
                input = {};
            }
            input[setting.name] = target.value;
            this.$emit('input', input);
        },
        on_bool: function (event) {
            var target = event.target;
            var input = _.cloneDeep(this.value);
            var setting = this.setting;
            if (input == null) {
                input = {};
            }
            input[setting.name] = target.checked;
            this.$emit('input', input);
        },
        on_radio: function (event) {
            var target = event.target;
            var input = _.cloneDeep(this.value);
            var setting = this.setting;
            if (input == null) {
                input = {};
            }
            if (setting.multiple) {
                if (!_.isArray(input[setting.name])) {
                    input[setting.name] = [];
                }
                var value = input[setting.name];
                if (target.checked) {
                    value.push(target.value);
                }
                else {
                    _.remove(value, function (val) {
                        return val == target.value;
                    });
                }
                input[setting.name] = value;
            }
            else {
                input[setting.name] = target.value;
            }
            this.$emit('input', input);
        },
        is_checked: function (key) {
            var config = this.config;
            if (_.isArray(config)) {
                var a = _.includes(config, key);
                return a;
            }
            else {
                var a = config == key;
                return a;
            }
        }
    },
    computed: {
        setting: function () {
            var settings = this.settings;
            var name = this.name;
            var found = _.find(settings, function (s) {
                return s.name == name;
            });
            return found;
        },
        config: function () {
            var configs = this.value;
            return configs[this.name];
        },
        input_type: function () {
            var setting = this.setting;
            if (setting.type == 'number') {
                return 'number';
            }
            else if (setting.type == 'text') {
                return 'text';
            }
            return null;
        },
        is_bool: function () {
            var setting = this.setting;
            return setting.type == 'bool';
        },
        is_select: function () {
            var setting = this.setting;
            return setting.type == 'select';
        },
        is_radio: function () {
            var setting = this.setting;
            return setting.type == 'radio';
        },
        radio_type: function () {
            var setting = this.setting;
            if (setting.multiple) {
                return 'checkbox';
            }
            else {
                return 'radio';
            }
        },
        id: function () {
            return this.app + "-" + this.setting.name;
        }
    },
    template: "<div class=\"form-group\">\n    <label v-if=\"setting.title != null && (input_type || is_select)\" :for=\"id\">{{ setting.title }}</label>\n    <label v-else-if=\"setting.title != null && is_radio\">{{ setting.title }}</label>\n\n    <input v-if=\"input_type\" :value=\"config\" @input=\"on_input\" \n            :type=\"input_type\" :name=\"setting.name\" :id=\"id\" :placeholder=\"setting.hint\" :disabled=\"!setting.enabled\"\n            class=\"form-control\" />\n    <div v-else-if=\"is_bool\" class=\"form-check\">\n        <input type=\"checkbox\" :name=\"setting.name\" :id=\"id\" @input=\"on_bool\" :checked=\"config\" :disabled=\"!setting.enabled\" \n                class=\"form-check-input\" :class=\"{'position-static': setting.title == null}\" :aria-label=\"setting.name\"/>\n        <label v-if=\"setting.title != null\" for=\"id\">{{ setting.title }}</label>\n    </div>\n    <select v-else-if=\"is_select\" :value=\"config\" @input=\"on_input\"\n            :name=\"setting.name\" :id=\"id\"\n            class=\"form-control\">\n        <option v-for=\"opt in setting.choices\" :key=\"opt.key\" :disabled=\"!opt.enabled\" :value=\"opt.key\">\n            {{ opt.value }}\n        </option>\n    </select>\n    <div v-else-if=\"is_radio\" v-for=\"opt in setting.choices\" :key=\"opt.key\"\n            class=\"form-check\">\n        <input :value=\"opt.key\" @input=\"on_radio\" :type=\"radio_type\" :checked=\"is_checked(opt.key)\"\n                :id=\"id + '-' + opt.key\" :name=\"setting.name\" :disabled=\"!opt.enabled\"\n                class=\"form-check-input\" />\n        <label :for=\"id + '-' + opt.key\"\n                class=\"form-check-label\">{{ opt.value }}</label>\n    </div>\n    <p v-else>There was an error parsing settings for {{ setting.name }} :/</p>\n</div>"
});
var setting_item = Vue.extend({
    props: {
        item: Object,
        settings: Array,
        value: Object,
        app: String
    },
    components: {
        'setting-value': setting_value
    },
    methods: {
        on_settings_changed: function (settings) {
            this.$emit('input', settings);
        }
    },
    template: "<div>\n    <hr v-if=\"item.type == 'divider'\">\n    <h4 v-else-if=\"item.type == 'header'\">{{ item.value }}</h4>\n    <p v-else-if=\"item.type == 'paragraph'\">{{ item.value }}</p>\n    <small v-else-if=\"item.type == 'info'\">{{ item.value }}</small>\n    <setting-value v-else-if=\"item.type == 'setting'\" :settings=\"settings\" :name=\"item.value\" :app=\"app\"\n            :value=\"value\" @input=\"on_settings_changed\" />\n    <setting-item v-else-if=\"item.type == 'group'\" v-for=\"(i, n) in item.value\" :key=\"n\" :settings=\"settings\" :item=\"i\" :app=\"app\"\n            :value=\"value\" @input=\"on_settings_changed\" />\n    <p v-else>An error occurred while parsing the item for <pre>{{ item }}</pre></p>\n</div>"
});
var setting_card = Vue.extend({
    props: {
        app: String,
        schema: String,
        starting_settings: {
            type: String,
            required: false
        },
        title: String
    },
    data: function () {
        return {
            settings: {},
            changed: false
        };
    },
    beforeMount: function () {
        if (this.starting_settings != null) {
            this.settings = JSON.parse(this.starting_settings);
        }
        else {
            this.load_settings();
        }
    },
    methods: {
        load_settings: function () {
            var self = this;
            console.log("Loading settings for " + this.app);
            $.ajax({
                url: "/api/settings/get/" + this.app,
                method: 'GET',
                success: function (data) {
                    self.settings = data;
                    self.changed = false;
                    console.log(self.settings);
                },
                error: function () {
                    console.error("Could not load settings for '" + self.app + "'");
                }
            });
        },
        on_settings_changed: function (new_settings) {
            this.settings = new_settings;
            this.changed = true;
        }
    },
    computed: {
        interface: function () {
            var schema = this.schema;
            if (typeof (schema) === 'string') {
                return JSON.parse(schema);
            }
            return schema;
        },
        items: function () {
            var schema = this.interface;
            return schema.items;
        },
        config: function () {
            var schema = this.interface;
            return schema.settings;
        }
    },
    components: {
        'setting-item': setting_item
    },
    template: "<div class=\"card\">\n    <div class=\"card-header\">\n        <h3>{{ title }}</h3>\n    </div>\n    <form action=\"#\">\n        <div class=\"card-body\">\n            <setting-item v-for=\"(i, n) in items\" :key=\"n\" :value=\"settings\" @input=\"on_settings_changed\" :item=\"i\" :settings=\"config\" :app=\"app\" />\n        </div>\n        <div class=\"card-footer\">\n            <button type=\"reset\" class=\"btn btn-danger ml-auto\" @click=\"load_settings\" :disabled=\"!changed\">Reset</button>\n        </div>\n    </form>\n</div>"
});
var app_settings = new Vue({
    el: '#app-settings',
    components: {
        'setting-card': setting_card
    }
});
