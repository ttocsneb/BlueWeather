
// Web

interface APIKey {
    name: string
    key: string
    permissions: Array<string>
}

interface SidebarItem {
    category: string
    value?: string
}

interface Web {
    static_url: string
    password_validation: Array<string>
    allowed_hosts: Array<string>
    sidebar: Array<SidebarItem>
    api_keys: Array<APIKey>
}

// Extensions

interface Extensions {
    weather_driver: string
    disabled: Array<string>
    settings: object
}

// Commands

interface Commands {
    stop: string
    restart: string
    shutdown: string
}

interface Config {
    debug: boolean
    time_zone: string
    web: Web
    extensions: Extensions
    commands: Commands
}