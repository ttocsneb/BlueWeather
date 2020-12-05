<template>
    <b-card no-body>
        <b-tabs card lazy>
            <b-tab
                title="Settings"
                active>
                <settings />
            </b-tab>
            <b-tab
                title="Plugins">
                <plugins />
            </b-tab>
        </b-tabs>
    </b-card>
</template>
<script lang="ts">
import Vue from 'vue'
import state from '../appState'

import plugins from './settings/plugins.vue'
import settings from './settings/settings.vue'

export default Vue.extend({
    data() {
        return {
            shared: state.state
        }
    },
    components: {
        plugins,
        settings
    }
})
</script>