<template>
    <b-navbar toggleable="sm" type="dark" variant="info">
        <b-navbar-brand href="#">BlueWeather</b-navbar-brand>

        <b-navbar-toggle target="navbar-collapse"></b-navbar-toggle>

        <b-collapse id="navbar-collapse" is-nav>
            <b-navbar-nav>
                <b-nav-item
                    v-if="shared.user.is_anonymous"
                    @click="login"
                    :disabled="shared.page_name == 'login'"
                    :class="{active: shared.page_name == 'login'}">
                    Login
                </b-nav-item>
                <b-nav-item
                    v-if="shared.user.is_authenticated"
                    @click="logout"
                    :class="{active: shared.page_name == 'login'}">
                    Logout
                </b-nav-item>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>
<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import state from './appState'
import login from './pages/login.vue'

export default Vue.extend({
    data() {
        return {
            shared: state.state
        }
    },
    methods: {
        login() {
            state.change_page(login, 'login')
        },
        logout() {

        }
    }
})
</script>