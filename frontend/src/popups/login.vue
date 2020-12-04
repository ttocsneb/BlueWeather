<template>
    <b-modal
        id="login"
        title="Login">
        <b-alert
            :show="error_message != null"
            variant="danger">{{ error_message }}</b-alert>
        <b-form-group
            label="Username"
            label-for="username">
            <b-form-input
                v-model="form.username"
                @keydown.enter="onSubmit"
                id="username"
                type="text"
                required
                placeholder="Username">
            </b-form-input>
        </b-form-group>
        <b-form-group
            label="Password"
            label-for="password">
            <b-form-input
                v-model="form.password"
                @keydown.enter="onSubmit"
                id="password"
                type="password"
                required
                placeholder="Password">
            </b-form-input>
        </b-form-group>

        <div slot="modal-footer">
            <b-button
                type="reset"
                @click="onCancel">
                Close
            </b-button>
            <b-button
                type="submit"
                variant="primary"
                @click="onSubmit">
                Login
            </b-button>
        </div>
    </b-modal>
</template>
<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import axios from 'axios'

import state from '../appState'
import {InvalidResponse} from '../types/response'
import {User} from '../types/user'

export default Vue.extend({
    data() {
        return {
            form: {
                username: '',
                password: ''
            },
            error_message: null,
            shared: state.state
        }
    },
    mounted() {
        this.$bvModal.show('login')
    },
    methods: {
        onSubmit() {
            if(!this.usernameValid || !this.passwordValid) {
                return
            }
            const self = this
            axios.post('/api/accounts/login/', this.form, {
                headers: {
                    'X-CSRFTOKEN': this.shared.token
                }
            }).then(resp => {
                let error = resp.data as InvalidResponse
                let data = resp.data as User
                if(error.code != undefined) {
                    self.error_message = error.detail
                    console.log(error.detail)
                    return
                }
                console.log(`Welcome ${data.name}`)
                self.shared.user = data
                self.onCancel()
            })
        },
        onCancel() {
            this.$bvModal.hide('login')
            this.form.username = ''
            this.form.password = ''
            this.error_message = null
        }
    },
    computed: {
        usernameValid() {
            return !_.isEmpty(this.form.username)
        },
        passwordValid() {
            return !_.isEmpty(this.form.password)
        }
    }
})
</script>