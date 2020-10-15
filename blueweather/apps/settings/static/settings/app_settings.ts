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
    title?: string
    default?: string
    enabled: boolean
    precision?: number
    range?: [number, number]
    hint?: string
    choices?: Array<Choice>
    multiple?: boolean
}

interface Item {
    type: 'divider' | 'header' | 'paragraph' | 'info' | 'setting'
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
        value: {},
        app: String
    },
    methods: {
        on_input(event: Event) {
            let target = event.target as any

            let value = target.value as string

            // TODO: Perform data validation

            this.$emit('input', value)
        },
        on_bool(event: Event) {
            let target = event.target as any

            let value = target.checked as boolean

            this.$emit('input', value)
        },
        on_radio(event: Event) {
            let target = event.target as any

            let input = this.value
            let setting = this.setting as SettingItem

            if(setting.multiple) {
                if(!_.isArray(input)) {
                    input = []
                }
                let value = input as Array<string>
                if(target.checked) {
                    value.push(target.value)
                } else {
                    _.remove(value, (val: string) => {
                        return val == target.value
                    })
                }
                input = value
            } else {
                input = target.value
            }

            this.$emit('input', input)
        },
        is_checked(key: string) {
            let config = this.value as Array<string> | string
            if(_.isArray(config)) {
                let a = _.includes(config, key)
                return a
            } else {
                let a = config == key
                return a
            }
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
            }
            return null
        },
        is_bool() {
            let setting = this.setting as SettingItem
            return setting.type == 'bool'
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
            if(setting.multiple) {
                return 'checkbox'
            } else {
                return 'radio'
            }
        },
        id() {
            return `${this.app}-${this.setting.name}`
        }
    },
    template: `<div class="form-group">
    <label v-if="setting.title != null && (input_type || is_select)" :for="id">{{ setting.title }}</label>
    <label v-else-if="setting.title != null && is_radio">{{ setting.title }}</label>

    <input v-if="input_type" :value="value" @input="on_input" 
            :type="input_type" :name="setting.name" :id="id" :placeholder="setting.hint" :disabled="!setting.enabled"
            class="form-control" />
    <div v-else-if="is_bool" class="form-check">
        <input type="checkbox" :name="setting.name" :id="id" @input="on_bool" :checked="value" :disabled="!setting.enabled" 
                class="form-check-input" :class="{'position-static': setting.title == null}" :aria-label="setting.name"/>
        <label v-if="setting.title != null" for="id">{{ setting.title }}</label>
    </div>
    <select v-else-if="is_select" :value="value" @input="on_input"
            :name="setting.name" :id="id"
            class="form-control">
        <option v-for="opt in setting.choices" :key="opt.key" :disabled="!opt.enabled" :value="opt.key">
            {{ opt.value }}
        </option>
    </select>
    <div v-else-if="is_radio" v-for="opt in setting.choices" :key="opt.key"
            class="form-check">
        <input :value="opt.key" @input="on_radio" :type="radio_type" :checked="is_checked(opt.key)"
                :id="id + '-' + opt.key" :name="setting.name" :disabled="!opt.enabled"
                class="form-check-input" />
        <label :for="id + '-' + opt.key"
                class="form-check-label">{{ opt.value }}</label>
    </div>
    <p v-else>There was an error parsing settings for {{ setting.name }} :/</p>
</div>`
})


const setting_item = Vue.extend({
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
        on_settings_changed(event: any) {
            let value = this.value as {[key: string]: any}
            value[this.item.value] = event
            this.$emit('input', value)
        }
    },
    template: `<div>
    <hr v-if="item.type == 'divider'">
    <h4 v-else-if="item.type == 'header'">{{ item.value }}</h4>
    <p v-else-if="item.type == 'paragraph'">{{ item.value }}</p>
    <small v-else-if="item.type == 'info'">{{ item.value }}</small>
    <setting-value v-else-if="item.type == 'setting'" :settings="settings" :name="item.value" :app="app"
            :value="value[item.value]" @input="on_settings_changed" />
    <setting-item v-else-if="item.type == 'group'" v-for="(i, n) in item.value" :key="n" :settings="settings" :item="i" :app="app"
            :value="value" @input="on_settings_changed" />
    <p v-else>An error occurred while parsing the item for <pre>{{ item }}</pre></p>
</div>`
})


const setting_card = Vue.extend({
    props: {
        app: String,
        schema: String,
        starting_settings: {
            type: String,
            required: false
        },
        title: String
    },
    data() {
        return {
            settings: {},
            changed: false
        }
    },
    created() {
        if(this.starting_settings != null) {
            this.settings = JSON.parse(this.starting_settings)
        } else {
            this.load_settings()
        }
    },
    methods: {
        load_settings() {
            let self = this
            $.ajax({
                url: `/api/settings/get/${this.app}`,
                method: 'GET',
                success(data: {[key: string]: any}) {
                    for(const prop in data) {
                        self.settings[prop] = data[prop]
                    }
                    self.changed = false
                },
                error() {
                    console.error(`Could not load settings for '${self.app}'`)
                }
            })
        },
        on_settings_changed(new_settings: object) {
            this.settings = JSON.parse(JSON.stringify(new_settings))
            this.changed = true
            this.$emit('modified')
        },
        save() {
            if(this.changed) {
                let self = this
                $.ajax({
                    url: `/api/settings/set/${this.app}`,
                    method: 'POST',
                    data: this.settings,
                    success(data: {[key: string]: any}) {
                        console.log(data)
                    },
                    error(jqXHR: JQuery.jqXHR, status: string, error: string) {
                        console.error(`An error occurred: ${status} - ${error}`)
                        console.log(jqXHR.responseJSON)
                        console.log(self.settings)
                    }
                })
            }
        }
    },
    computed: {
        interface() {
            let schema = this.schema as string
            if(typeof(schema) === 'string') {
                return JSON.parse(schema)
            }
            // TODO parse the schema into form-groups
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
        <h3>{{ title }}</h3>
    </div>
    <form action="#">
        <div class="card-body">
            <setting-item v-for="(i, n) in items" :key="n" :value="settings" @input="on_settings_changed" :item="i" :settings="config" :app="app" />
        </div>
    </form>
</div>`
})


const app_settings = new Vue({
    el: '#app-settings',
    data() {
        return {
            modified: false
        }
    },
    methods: {
        on_modified() {
            this.modified = true
        },
        save() {
            let children = this.$children as Array<any>
            for(const i in children) {
                children[i].save()
            }
            this.modified = false
        }
    },
    computed: {
        save_class() {
            if(this.modified) {
                return []
            } else {
                return ['d-none']
            }
        }
    },
    components: {
        'setting-card': setting_card
    }
})