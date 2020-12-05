
export interface InvalidResponse {
    code: number
    detail: string
}


export interface Validation {
    [key: string]: Array<string> | Validation
}


export interface ValidateResponse extends InvalidResponse {
    validation: Validation
}

export interface PagifyResponse {
    page: number
    size: number
    pages: number
    total: number
}
