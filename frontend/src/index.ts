import Vue from 'vue'
import app from './app.vue'
import {BootstrapVue} from 'bootstrap-vue'


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