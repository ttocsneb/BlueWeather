import {User} from './types/user'

declare var __user__: User


function log(name: string, data: any = undefined) {
    if(data !== undefined) {
        console.log(`${name} triggered with`)
        console.log(data)
    } else {
        console.log(`${name} triggered`)
    }
}


export default {
    debug: true,
    state: {
        user: __user__,
        page: null,
        page_name: null as string
    },
    change_page(page: any, name: string) {
        if(this.debug) log('change_page', {page, name})
        this.state.page = page
        this.state.page_name = name
    }

}