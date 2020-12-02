<template>
    <b-card
        title="Login">
        <b-card-body>
            <div class="row">
                <b-form
                    @submit="onSubmit"
                    class="col-12 col-md-6 col-lg-4">
                    <b-form-group
                        id="username-group"
                        label="Username"
                        label-for="username">
                        <b-form-input
                            id="username"
                            v-model="form.username"
                            type="text"
                            required
                            placeholder="Username">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group
                        id="password-group"
                        label="Password"
                        label-for="password">
                        <b-form-input
                            id="password"
                            v-model="form.password"
                            type="password"
                            required
                            placeholder="Password">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group
                        id="action-group">
                        <b-button type="submit" variant="primary">Login</b-button>
                    </b-form-group>
                </b-form>
            </div>
        </b-card-body>
    </b-card>
</template>
<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    data() {
        return {
            form: {
                username: "hello",
                password: "bar"
            }
        }
    },
    methods: {
        onSubmit() {
            console.log("Login submitted")
        }
    }
})
</script>