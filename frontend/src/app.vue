<template>
    <div>
        <navbar />
        <div class="container">
            <component :is="page" />
        </div>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import navbar from './navbar.vue'
import login from './pages/login.vue'

export default Vue.extend({
    data() {
        return {
            page: login
        }
    },
    components: {
        navbar
    }
})
</script>