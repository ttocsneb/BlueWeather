
export interface User {
    username: string
    name?: string
    is_active: boolean
    is_anonymous: boolean
    is_authenticated: boolean
    is_staff: boolean
    is_superuser: boolean
    last_login?: string
}

declare var __user__: User

export const user = __user__
