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
    pageSize: Number
  },
  template: `<p><p>`
})

const plugin_item = Vue.extend({
  props: {
    plugin: Object,
  },
  template: `<li class="list-group-item">
  <h3>{{ plugin.name }}</h3>
  <p v-if="plugin.info.summary">{{ plugin.info.summary }}</p>
  <ul>
    <li v-if="plugin.info.version">Version: {{ plugin.info.version }}</li>
    <li v-if="plugin.info.homepage">homepage: {{ plugin.info.homepage }}</li>
    <li v-if="plugin.info.author">author: {{ plugin.info.author }}</li>
    <li v-if="plugin.info.email">email: {{ plugin.info.email }}</li>
    <li v-if="plugin.info.license">license: {{ plugin.info.license }}</li>
  </ul>
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
      pages: 0,
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
    getData(page: number = 0) {
      const self = this;
      $.ajax({
        url: "/api/plugins/list",
        type: "get",
        data: {
          page: page,
          items: self.pageSize
        },
        success: function(data: PluginListResponse) {
          self.plugins = data.plugins
          self.page = data.page
          self.pages = data.pages
          console.log(data)
        }
      })
    },
    first() {
      this.getData(0);
    },
    last() {
      this.getData(this.pages - 1);
    },
    next() {
      this.getData(Math.min(this.page + 1, this.pages - 1));
    },
    prev() {
      this.getData(Math.max(this.page - 1, 0))
    }
  },
  computed: {
    pageList() {
      const display = 5;
      const half = Math.floor(display / 2);
      // Get the first number of the index
      const start = Math.min(Math.max(this.page - half, 0), this.page + half, Math.max(this.pages - display, 0));
      // get the size of the index
      const size = Math.min(display, this.pages - start);
      return _.range(start, start + size);
    }
  }
});
