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

type Pages = {[key: string]: any}

const params = new URLSearchParams(window.location.search)


var state = {
    debug: true,
    state: {
        user: __user__,
        token: __token__,
        page: params.get('page') as string,
        popup: null as any,
        pages: {} as Pages,
        params: params
    },
    events: {} as Events,
    /**
     * Change the page
     * 
     * @param page page component
     * @param name name of the page
     */
    change_page(page: string) {
        if(this.debug) log('change_page', page)
        this.state.params.set('page', page)
        window.history.pushState({page: page}, '', `?${this.state.params.toString()}`)
        this.state.page = page
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
    },
    register_page(name: string, page: any) {
        if(this.debug) log('register_page', {name})
        this.state.pages[name] = page
    }
}

window.addEventListener('popstate', (ev) => {
    if(ev.state.page != undefined) {
        state.state.page = ev.state.page
        state.state.params.set('page', state.state.page)
    }
})

export default state