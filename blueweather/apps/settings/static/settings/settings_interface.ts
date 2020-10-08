

interface Choice {
    key: string
    value: String
    enabled: boolean
}


interface SettingItem {
    name: string
    type: 'number' | 'select' | 'text' | 'radio' | 'bool'
    default: string
    enabled: boolean
    options: {
        precision?: number
        range?: [number, number]
        hint?: string
        choices?: Array<Choice>
        multiple?: boolean
    }
}

interface StringItem {
    type: 'header' | 'label' | 'info' | 'setting'
    value: string
}

interface DividerItem {
    type: 'divider'
}

interface GroupItem {
    type: 'group'
    value: Item
}

type Item = StringItem | DividerItem | GroupItem 

interface Settings {
    settings: Array<SettingItem>
    items: Array<Item>
}