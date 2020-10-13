/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />


interface Plugin {
  pluginName: string
  enabled: string
  extensions: Array<string>
  info: {
    packageName: string
    version?: string
    summary?: string
    homepage?: string
    author?: string
    email?: string
    license?: string
    description?: string
  }
}

interface PluginListResponse {
  plugins: Array<Plugin>
  pages: number
  page: number
}


const plugin_header = Vue.extend({
  props: {
    page: Number,
    pages: Number,
    page_size: Number
  },
  watch: {
    page_size: {
      immediate: true,
      handler(newVal: number, oldVal: number) {
        this.pageSize = newVal.toString()
      }
    },
    pageSize(newVal: string, oldVal: string) {
      if(newVal != this.page_size) {
        this.$emit('set-size', parseInt(newVal))
      }
    }
  },
  data() {
    return {
      pageSize: '10'
    }
  },
  computed: {
    page_numbers() {
      const n = 3

      let start = Math.max(0, Math.floor(this.page - n / 2))
      let end = Math.min(this.pages, start + n)

      return _.range(start, end)
    }
  },
  methods: {
    activeClass(enabled: boolean) {
      if(enabled) {
        return [
          'text-primary'
        ]
      } else {
        return [
          'btn-primary'
        ]
      }
    },
    endsClass(enabled: boolean) {
      if(enabled) {
        return [
          'text-primary'
        ]
      } else {
        return [
          'text-secondary'
        ]
      }
    },
    enabled(index: number) {
      return index != this.page
    },
    setPage(index: number) {
      this.$emit('set-page', index)
    }
  },
  template: `<form class="form-inline" action="#">
  <div class="form-group mb-0 ml-sm-auto mr-auto mr-sm-0 mt-2 mt-sm-0">
    <select v-model="pageSize" class="form-control">
      <option>1</option>
      <option>2</option>
      <option>4</option>
      <option>5</option>
      <option>10</option>
      <option>25</option>
      <option>50</option>
      <option>100</option>
    </select>
  </div>
  <div class="form-group mb-0 ml-3">
    <button role="button" class="btn"
        :class="endsClass(enabled(0))"
        :disabled="!enabled(0)"
        @click="setPage(0)">
      <i class="fas fa-chevron-left"></i>
    </button>
    <button v-for="i in page_numbers" 
        :class="activeClass(enabled(i))"
        :disabled="!enabled(i)"
        @click="setPage(i)"
          role="button" class="btn">{{ i + 1 }}</button>
    <button role="button" class="btn"
        :class="endsClass(enabled(pages - 1))"
        :disabled="!enabled(pages - 1)"
        @click="setPage(pages - 1)">
      <i class="fas fa-chevron-right"></i>
    </button>
  </div>
</form>`
})

const plugin_item = Vue.extend({
  props: {
    plugin: Object,
  },
  computed: {
    badges() {
      let badges = []

      if(this.plugin.builtin) {
        badges.push({
          color: 'secondary',
          value: 'builtin'
        })
      }

      if(!this.plugin.enabled) {
        badges.push({
          color: 'warning',
          value: 'disabled'
        })
      }

      return badges
    },
    homepage() {
      if(this.plugin.info.homepage == null) {
        return null
      }
      let url = new URL(this.plugin.info.homepage)
      return url.host
    }
  },
  template: `<li class="list-group-item">
  <!-- Header -->
  <div class="mb-2">
    <h4 class="d-inline mb-0">{{ plugin.pluginName }}</h4>
    <small v-if="plugin.pluginName != plugin.info.packageName" class="d-inline">
    - {{ plugin.info.packageName }}
    </small>

    <!-- Badges -->
    <div class="float-md-right">
      <span v-for="badge in badges"
          :class="'badge-' + badge.color"
          class="d-inline badge ml-2">{{ badge.value }}</span>
    </div>
  </div>
  <p v-if="plugin.info.summary">{{ plugin.info.summary }}</p>

  <!-- Footer -->
  <div>
    <small v-if="plugin.info.version" 
        class="d-inline mr-2">
      <i class="fas fa-pen"></i>
      {{ plugin.info.version }}
    </small>
    <small v-if="plugin.info.homepage"
        class="d-inline mr-2">
      <i class="fas fa-home"></i>
      <a :href="plugin.info.homepage" target="_blank">{{ homepage }}</a>
    </small>
    <small v-if="plugin.info.author"
        class="d-inline mr-2">
      <i class="fas fa-address-book"></i>
      {{ plugin.info.author }}
    </small>
    <small v-if="plugin.info.license"
        class="d-inline">
      <i class="fas fa-file-contract"></i>
      {{ plugin.info.license }}
    </small>
  </div>
</li>
`
})

const plugin_body = Vue.extend({
  props: {
    plugins: Array
  },
  components: {
    'plugin-item': plugin_item
  },
  template: `<ul class="list-group list-group-flush">
  <plugin-item :plugin="plugin" 
      v-for="plugin in plugins" />
</ul>
`
})

var plugin_list = new Vue({
  el: '#plugin-list',
  data() {
    return {
      plugins: {},
      pages: 1,
      page: 0,
      pageSize: 10
    }
  },
  components: {
    'plugin-header': plugin_header,
    'plugin-body': plugin_body
  },
  beforeMount() {
    this.getData();
  },
  methods: {
    getData() {
      const self = this;
      $.ajax({
        url: "/api/plugins/list",
        type: "get",
        data: {
          page: self.page,
          size: self.pageSize
        },
        success: function(data: PluginListResponse) {
          self.plugins = data.plugins
          self.page = data.page
          self.pages = data.pages
        }
      })
    },
    setPage(page: number) {
      this.page = page
      this.getData()
    },
    setPageSize(size: number) {
      this.pageSize = size
      this.getData()
    }
  }
});
