import Vue from 'vue'
import app from './app.vue'
import {BootstrapVue} from 'bootstrap-vue'

import state from './appState'
import settings from './pages/settings.vue'


state.register_page('settings', settings)


Vue.use(BootstrapVue)


new Vue({
    el: '#app',
    data() {
        return {
            page: '',
            modal: null
        }
    },
    methods: {
        onUser(action: string) {
            if(action == "login") {
                this.modal = 'login'
                
            }
        },
        changePage(page: string) {
            this.page = page
        }
    },
    components: {
        app
    }
})