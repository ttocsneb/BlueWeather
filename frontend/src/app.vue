<template>
    <div>
        <navbar />
        <div class="container">
            <component :is="shared.page" />
        </div>
        <template>
            <component :is="shared.popup" />
        </template>
        <template>
            <disconect />
        </template>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import navbar from './navbar.vue'
import login from './pages/login.vue'
import state from './appState'
import Disconect from './popups/disconect.vue'

export default Vue.extend({
    data() {
        return {
            shared: state.state
        }
    },
    components: {
        navbar,
        Disconect
    },
})
</script>