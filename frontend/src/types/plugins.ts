import {PagifyResponse} from './response'

export interface InfoItem {
    packageName: string
    label: string
    version: string
    summary: string
    homepage: string
    author: string
    email: string
    license: string
    description: string
}

export interface InfoResponse extends PagifyResponse {
    info: Array<InfoItem>
}