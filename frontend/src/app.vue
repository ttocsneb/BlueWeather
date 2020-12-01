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

export default Vue.extend({
    data() {
        return {
            page: null
        }
    },
    components: {
        navbar
    }
})
</script>