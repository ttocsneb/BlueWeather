var setting_value = Vue.extend({
    props: {
        name: String,
        settings: Array,
        value: {
            default: {},
            type: Object
        }
    },
    methods: {
        on_input: function (event) {
            var input = this.value;
            if (input == null) {
                input = {};
            }
            var setting = this.setting;
            var target = event.target;
            console.log(target);
            input[setting.name] = target.value;
            console.log(input);
            this.$emit('input', input);
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
        input_type: function () {
            var setting = this.setting;
            if (setting.type == 'number') {
                return 'number';
            }
            else if (setting.type == 'text') {
                return 'text';
            }
            else if (setting.type == 'bool') {
                return 'checkbox';
            }
            return null;
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
            if (setting.options.multiple) {
                return 'checkbox';
            }
            else {
                return 'radio';
            }
        }
    },
    template: "<div>\n    <input v-if=\"input_type\" :value=\"setting.value\" @input=\"on_input\" :type=\"input_type\" :name=\"setting.name\" :placeholder=\"setting.options.hint\" :disabled=\"!setting.enabled\"\n            class=\"form-control\" />\n    <select v-else-if=\"is_select\" :value=\"setting.value\" @input=\"on_input\" :name=\"setting.name\"\n            class=\"form-control\">\n        <option v-for=\"opt in setting.options.choices\" :key=\"opt.key\" :disabled=\"!opt.enabled\" :value=\"opt.key\">{{ opt.value }}</option>\n    </select>\n    <div v-else-if=\"is_radio\" v-for=\"opt in setting.options.choices\" :key=\"opt.key\"\n            class=\"form-group\">\n        <input :value=\"opt.key\" @input=\"on_input\" :type=\"radio_type\" :id=\"opt.key\" :name=\"setting.name\" :disabled=\"!opt.enabled\"\n                class=\"form-control\" />\n        <label :for=\"opt.key\">{{ opt.value }}</label>\n    </div>\n    <p v-else>There was an error parsing settings for {{ setting.name }} :/</p>\n</div>"
});
var setting_item = Vue.extend({
    props: {
        item: Object,
        settings: Array,
        value: Object
    },
    components: {
        'setting-value': setting_value
    },
    template: "<div class=\"form-group\">\n    <hr v-if=\"item.type == 'divider'\">\n    <h4 v-else-if=\"item.type == 'header'\">{{ item.value }}</h4>\n    <label v-else-if=\"item.type == 'label'\">{{ item.value }}</label>\n    <small v-else-if=\"item.type == 'info'\">{{ item.value }}</small>\n    <setting-value v-else-if=\"item.type == 'setting'\" :settings=\"settings\" :name=\"item.value\"\n            :value=\"value\" @input=\"$emit('input', $event)\" />\n    <setting-item v-else-if=\"item.type == 'group'\" v-for=\"(i, n) in item.value\" :key=\"n\" :settings=\"settings\" :item=\"i\"\n            :value=\"value\" @input=\"$emit('input', $event)\" />\n    <p v-else>An error occurred while parsing the item for <pre>{{ item }}</pre></p>\n</div>"
});
var setting_card = Vue.extend({
    props: {
        app: String,
        schema: String
    },
    data: function () {
        return {
            settings: {},
        };
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
    template: "<div class=\"card\">\n    <div class=\"card-header\">\n        <h3>{{ app }}</h3>\n    </div>\n    <div class=\"card-body\">\n        <form>\n            <setting-item v-for=\"(i, n) in items\" :key=\"n\" v-model=\"settings\" :item=\"i\" :settings=\"config\" />\n        </form>\n    </div>\n</div>"
});
var app_settings = new Vue({
    el: '#app-settings',
    components: {
        'setting-card': setting_card
    }
});
