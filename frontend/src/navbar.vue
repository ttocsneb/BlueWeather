<template>
    <b-navbar toggleable="sm" type="dark" variant="info">
        <b-navbar-brand href="#">BlueWeather</b-navbar-brand>

        <b-navbar-toggle target="navbar-collapse"></b-navbar-toggle>

        <b-collapse id="navbar-collapse" is-nav>
            <b-navbar-nav>
                <b-nav-item href="#">Link</b-nav-item>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>
<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    data() {
        return {}
    }
})
</script>