/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />

interface PluginItem {
  human_name: string;
  description: string;
  author: string;
  url: string;
  entrypoints: Array<string>;
  builtin: boolean;
}
type PluginList = {[key: string]: PluginItem}
interface PluginResponse {
  plugins: PluginList;
  page: number;
  items: number;
  pages: number;
  total: number;
}

const plugin_list_component = Vue.extend({
  props: {
    extensions: Object,
  },
  template: `
<div id="plugin-list-accordion">
  <div class="card" v-for="(ext, name) in extensions">
    <div class="card-header">
      <h5 class="mb-0" :id="'heading' + name">
              <button class="btn btn-link collapsed" data-toggle="collapse" :data-target="'#collapse' + name" aria-expanded="false" :aria-controls="'collapse' + name">
                {{ ext.human_name }}
                <span v-if="ext.builtin" class="badge badge-secondary">builtin</span>
              </button>
      </h5>
    </div>
    <div :id="'collapse' + name" class="collapse" :aria-labelledby="'heading' + name" data-parent="#plugin-list-accordion">
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <p>{{ ext.description }}</p>
          <p v-if="ext.author != null">Author: {{ ext.author }}</p>
          <p v-if="ext.url != null"><a :href="ext.url">{{ ext.url }}</a></p>
        </li>
      </ul>
      <div class="card-body">
        <h6>Entry Points</h6>
        <ul>
          <li v-for="point in ext.entrypoints">
            <h6>{{ point }}</h6>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
`
});

var plugin_list = new Vue({
  el: '#plugin-list',
  data: function name() {
    return {
      extensions: {},
      pages: 0,
      page: 0,
      total: 0,
      items: 0,
      pageSize: 10
    }
  },
  components: {
    'plugin-list': plugin_list_component
  },
  beforeMount: function () {
    this.getData();
  },
  methods: {
    getData: function(page: number = 0) {
      const _this = this;
      $.ajax({
        url: "/api/plugins/list",
        type: "get",
        data: {
          page: page,
          items: _this.pageSize
        },
        success: function(data: PluginResponse) {
          _this.extensions = data.plugins;
          _this.page = data.page;
          _this.items = data.items;
          _this.pages = data.pages;
          _this.total = data.total;
        }
      })
    },
    first: function() {
      this.getData(0);
    },
    last: function() {
      this.getData(this.pages - 1);
    },
    next: function() {
      this.getData(Math.min(this.page + 1, this.pages - 1));
    },
    prev: function() {
      this.getData(Math.max(this.page - 1, 0))
    }
  },
  computed: {
    pageList: function() {
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
