import {User} from './types/user'
import _ from 'lodash'
import {AxiosError} from 'axios'

declare var __user__: User
declare var __token__: string

function log(name: string, data: any = undefined) {
    if(data !== undefined) {
        console.log(`${name} triggered with`)
        console.log(data)
    } else {
        console.log(`${name} triggered`)
    }
}

type Events = {[key: string]: Array<CallableFunction>}


export default {
    debug: true,
    state: {
        user: __user__,
        token: __token__,
        page: null,
        page_name: null as string,
        popup: null
    },
    events: {} as Events,
    /**
     * Change the page
     * 
     * @param page page component
     * @param name name of the page
     */
    change_page(page: any, name: string) {
        if(this.debug) log('change_page', {page, name})
        this.state.page = page
        this.state.page_name = name
    },
    /**
     * Change the active popup, note that this will not open the popup
     * 
     * @param popup popup component
     */
    change_popup(popup: any) {
        if(this.debug) log('change_popup', popup)
        this.state.popup = popup
    },
    /**
     * Register an event
     * @param name name of the event
     * @param event event
     */
    register_event(name: string, event: CallableFunction) {
        if(!this.events.hasOwnProperty(name)) {
            this.events[name] = []
        }
        if(!_.includes(this.events[name], event)) {
            this.events[name].push(event)
        }
    },
    /**
     * Unregister an event
     * @param name name of the event
     * @param event event
     */
    unregister_event(name: string, event: CallableFunction) {
        if(!this.events.hasOwnProperty(name)) {
            return
        }
        _.remove(this.events[name], e => e == event)
    },
    /**
     * Call an event
     * @param name name of the event
     */
    event(name: string) {
        if(this.events.hasOwnProperty(name)) {
            for(let event of this.events[name]) {
                event()
            }
        }
    },
    handleHttpError(error: AxiosError) {
        if(error.response) {
            if(error.response.status == 403) {
                // The csrf token has probably been outdated
                window.location.reload()
            }
        } else if(error.request) {
            // The server was disconnected
            this.event('disconnect')
        } else {
            // Something happened in setting up the request
        }
    }
}