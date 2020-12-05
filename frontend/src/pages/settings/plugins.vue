<template>
    <div>
        <div class="d-flex flex-row">
            <b-form-select
                v-model="form.size"
                :options="sizes"
                class="w-auto ml-auto mr-3" />
            <b-pagination
                v-model="form.page"
                :total-rows="pages"
                :per-page="pageSize"
                :disabled="!loaded"
                class="mb-0">
            </b-pagination>
        </div>
        <hr>
        <b-list-group flush>
            <b-list-group-item
                v-for="plugin in plugins"
                :key="plugin.label">
                <h4>{{ plugin.label }}</h4>
                <p>{{ plugin.summary }}</p>
                <div v-html="plugin.description"
                    v-if="isDescToggled(plugin.label)">
                </div>
                <p><a href="#"
                    @click="toggleDesc(plugin.label)">
                    <span v-if="isDescToggled(plugin.label)">
                    Less
                    </span>
                    <span v-else>More</span>
                </a></p>
                <div>
                    <div
                        v-for="badge in filter_badges(plugin)"
                        :key="badge.name"
                        class="badge mr-2 p-1"
                        :class="'badge-' + badge.variant">
                        <i :class="badge.icon"></i>
                        {{ plugin[badge.name] }}
                    </div>
                    <a class="badge badge-success p-1"
                        :href="plugin.homepage"
                        target="_blank">
                        <i class="fas fa-home"></i>
                        Homepage
                    </a>
                </div>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import _ from 'lodash'

import state from '../../appState'

import {InfoResponse, InfoItem} from '../../types/plugins'

interface Badge {
    name: string
    icon: string
    variant: string
}

export default Vue.extend({
    data() {
        return {
            plugins: [],
            shared: state.state,
            page: 1,
            pageSize: 10,
            total: 0,
            pages: 0,
            loaded: false,
            form: {
                page: 1,
                size: 10
            },
            badges: [
                {
                    name: 'version',
                    icon: 'fas fa-code-branch',
                    variant: 'primary'
                },
                {
                    name: 'author',
                    icon: 'fas fa-user-edit',
                    variant: 'info'
                },
                {
                    name: 'license',
                    icon: 'fas fa-balance-scale',
                    variant: 'secondary'
                }
            ],
            sizes: [
                {value: -1, text: 'all'},
                10, 20, 50, 100
            ],
            toggled_descs: []
        }
    },
    watch: {
        form: {
            deep: true,
            handler(val, oldval) {
                this.loadPlugins()
            }
        },
        selected_page(newPage: number, oldPage: number) {
            this.page = newPage
            this.loadPlugins()
        }
    },
    beforeMount() {
        this.onDisplay()
    },
    methods: {
        loadPlugins() {
            this.loaded = false
            let params = new URLSearchParams()
            params.set('page', String(this.form.page - 1))
            params.set('size', this.form.size)
            let self = this
            axios.get(`/api/plugins/info/?${params.toString()}`).then(response => {
                let data = response.data as InfoResponse
                self.page = data.page
                self.form.page = data.page + 1
                self.pageSize = data.size
                self.form.size = data.size
                self.total = data.total
                self.pages = data.pages
                self.plugins = data.info
                self.loaded = true
                console.log(data)
            }).catch(error => {
                self.loaded = false
                state.handleHttpError(error)
            })
        },
        onDisplay() {
            if(!this.loaded) {
                this.loadPlugins()
            }
        },
        filter_badges(item: InfoItem) {
            let i = item as any
            return _.filter(this.badges, (b: Badge) => i[b.name] != null)
        },
        toggleDesc(name: string) { 
            if(this.isDescToggled(name)) {
                let i = _.indexOf(this.toggled_descs, name)
                this.$delete(this.toggled_descs, i)
            } else {
                this.toggled_descs.push(name)
            }
            console.log(this.toggled_descs)
            console.log(this.isDescToggled(name))
        },
        isDescToggled(name: string) {
            return this.toggled_descs.includes(name)
        }
    }
})
</script>