import Vue from 'vue'
import Login from './login/login.vue'
import {modal, navbar} from 'vue-strap'


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
        onPage(page: string) {

        }
    },
    components: {
        navbar: navbar,
        login: Login,
        modal: modal
    }
})