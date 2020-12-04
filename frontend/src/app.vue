<template>
    <div>
        <navbar />
        <div class="container">
            <component :is="shared.page" />
        </div>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import navbar from './navbar.vue'
import login from './pages/login.vue'
import state from './appState'

export default Vue.extend({
    data() {
        return {
            shared: state.state
        }
    },
    components: {
        navbar
    }
})
</script>