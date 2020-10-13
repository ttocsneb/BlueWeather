/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />
/// <reference types="bootstrap" />

interface Choice {
    key: string
    value: string
    enabled: boolean
}

interface SettingItem {
    name: string
    type: 'number' | 'select' | 'text' | 'radio' | 'bool'
    default?: string
    enabled: boolean
    options: {
        precision?: number
        range?: [number, number]
        hint?: string
        choices?: Array<Choice>
        multiple?: boolean
    }
}

interface Item {
    type: 'divider' | 'header' | 'label' | 'info' | 'setting'
    value: string
}

interface GroupItem {
    type: 'group'
    value: Array<Conf>
}

type Conf = Item | GroupItem

interface Schema {
    settings: Array<SettingItem>
    items: Array<Conf>
}


const setting_value = Vue.extend({
    props: {
        name: String,
        settings: Array,
        value: {
            default: {},
            type: Object
        }
    },
    methods: {
        on_input(event: Event) {
            let input = this.value as {[key: string]: any}
            if(input == null) {
                input = {}
            }
            let setting = this.setting as SettingItem
            let target = event.target as any

            console.log(target)
            // TODO: Check if the value for the multi-choice options is a string or array
            // TODO: Perform data validation

            input[setting.name] = target.value
            console.log(input)
            this.$emit('input', input)
        }
    },
    computed: {
        setting() {
            let settings = this.settings as Array<SettingItem>
            let name = this.name as string
            let found = _.find(settings, (s: SettingItem) => {
                return s.name == name
            })
            return found
        },
        input_type() {
            let setting = this.setting as SettingItem
            if(setting.type == 'number') {
                return 'number'
            } else if(setting.type == 'text') {
                return 'text'
            } else if(setting.type == 'bool') {
                return 'checkbox'
            }
            return null
        },
        is_select() {
            let setting = this.setting as SettingItem
            return setting.type == 'select'
        },
        is_radio() {
            let setting = this.setting as SettingItem
            return setting.type == 'radio'
        },
        radio_type() {
            let setting = this.setting as SettingItem
            if(setting.options.multiple) {
                return 'checkbox'
            } else {
                return 'radio'
            }
        }
    },
    template: `<div>
    <input v-if="input_type" :value="setting.value" @input="on_input" :type="input_type" :name="setting.name" :placeholder="setting.options.hint" :disabled="!setting.enabled"
            class="form-control" />
    <select v-else-if="is_select" :value="setting.value" @input="on_input" :name="setting.name"
            class="form-control">
        <option v-for="opt in setting.options.choices" :key="opt.key" :disabled="!opt.enabled" :value="opt.key">{{ opt.value }}</option>
    </select>
    <div v-else-if="is_radio" v-for="opt in setting.options.choices" :key="opt.key"
            class="form-group">
        <input :value="opt.key" @input="on_input" :type="radio_type" :id="opt.key" :name="setting.name" :disabled="!opt.enabled"
                class="form-control" />
        <label :for="opt.key">{{ opt.value }}</label>
    </div>
    <p v-else>There was an error parsing settings for {{ setting.name }} :/</p>
</div>`
})


const setting_item = Vue.extend({
    props: {
        item: Object,
        settings: Array,
        value: Object
    },
    components: {
        'setting-value': setting_value
    },
    template: `<div class="form-group">
    <hr v-if="item.type == 'divider'">
    <h4 v-else-if="item.type == 'header'">{{ item.value }}</h4>
    <label v-else-if="item.type == 'label'">{{ item.value }}</label>
    <small v-else-if="item.type == 'info'">{{ item.value }}</small>
    <setting-value v-else-if="item.type == 'setting'" :settings="settings" :name="item.value"
            :value="value" @input="$emit('input', $event)" />
    <setting-item v-else-if="item.type == 'group'" v-for="(i, n) in item.value" :key="n" :settings="settings" :item="i"
            :value="value" @input="$emit('input', $event)" />
    <p v-else>An error occurred while parsing the item for <pre>{{ item }}</pre></p>
</div>`
})


const setting_card = Vue.extend({
    props: {
        app: String,
        schema: String
    },
    data() {
        return {
            settings: {},
        }
    },
    computed: {
        interface() {
            let schema = this.schema as string
            if(typeof(schema) === 'string') {
                return JSON.parse(schema)
            }
            return schema
        },
        items() {
            let schema = this.interface as Schema
            return schema.items
        },
        config() {
            let schema = this.interface as Schema
            return schema.settings
        }
    },
    components: {
        'setting-item': setting_item
    },
    template: `<div class="card">
    <div class="card-header">
        <h3>{{ app }}</h3>
    </div>
    <div class="card-body">
        <form>
            <setting-item v-for="(i, n) in items" :key="n" v-model="settings" :item="i" :settings="config" />
        </form>
    </div>
</div>`
})


const app_settings = new Vue({
    el: '#app-settings',
    components: {
        'setting-card': setting_card
    }
})