
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
