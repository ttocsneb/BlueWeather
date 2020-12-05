<template>
    <b-navbar toggleable="sm" type="dark" variant="info">
        <b-navbar-brand
            href="#"
            @click="home">
            BlueWeather
        </b-navbar-brand>

        <b-navbar-toggle
            target="navbar-collapse">
        </b-navbar-toggle>

        <b-collapse
            id="navbar-collapse"
            is-nav>
            <b-navbar-nav
                class="w-100">
                <b-nav-item
                    v-if="shared.user.is_authenticated"
                    @click="settings"
                    :class="{active: shared.page_name == 'settings'}"
                    class="mr-sm-auto">
                    Settings
                </b-nav-item>
                <b-nav-item
                    v-if="shared.user.is_anonymous"
                    @click="login"
                    class="ml-sm-auto">
                    Login
                </b-nav-item>
                <b-nav-item
                    v-if="shared.user.is_authenticated"
                    @click="logout">
                    Logout
                </b-nav-item>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>
<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import axios from 'axios'

import state from './appState'
import login from './popups/login.vue'

import {User} from './types/user'

export default Vue.extend({
    data() {
        return {
            shared: state.state
        }
    },
    methods: {
        login() {
            state.change_popup(login)
            this.$bvModal.show('login')
        },
        logout() {
            const self = this
            axios.get('/api/accounts/logout').then(res => {
                let data = res.data as User
                self.shared.user = data
            }).catch(err => {
                state.handleHttpError(err)
            })
        },
        home() {
            state.change_page("home")
        },
        settings() {
            state.change_page("settings")
        }
    }
})
</script>