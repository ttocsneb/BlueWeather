<template>
    <b-modal
        id="disconnect"
        title="Disconnected"
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close>
        The server has been disconnected.
        <div slot="modal-footer">
            <b-button
                type="button"
                @click="reload">Reload</b-button>
        </div>
    </b-modal>
</template>
<script lang="ts">
import Vue from 'vue'
import axios from 'axios'

import state from '../appState'

export default Vue.extend({
    beforeMount() {
        state.register_event('disconnect', this.onDisconnect)
    },
    methods: {
        onDisconnect() {
            this.$bvModal.show('disconnect')
            setInterval(() => {
                axios.get('/api/accounts/status').then(resp => {
                    window.location.reload()
                })
            }, 5000)
        },
        reload() {
            window.location.reload()
        }
    }
})
</script>