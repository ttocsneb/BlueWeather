// API

type SuccessCallback = (data: ApplyResponse, textStatus: string, jqXHR: JQueryXHR) => void
type ErrorCallback = (jqXHR: JQueryXHR, textStatus: String, errorThrown: string) => void

interface UpdateSettings {
    data: object
    namespace?: string
    success?: SuccessCallback
    error?: ErrorCallback
}

interface ValidationObject {[key: string]: ValidationType}
type ValidationType = Array<String> | ValidationObject

interface ApplyResponse {
    success: boolean,
    reason?: string,
    validation?: ValidationType,
    namespace?: string,
    settings?: {[key: string]: any}
}

declare function update_settings(config: UpdateSettings): void
declare function validationToString(error: ValidationType, base?: string): string

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