/// <reference types="vue" />
/// <reference types="jquery" />
/// <reference types="lodash" />
/// <reference types="settings" />


const plugin_list_component = Vue.extend({
  props: {
    extension: Object,
    name: String
  },
  computed: {
    disableValue: function() {
      return this.extension.enabled ? "Disable" : "Enable";
    },
    disableClass: function() {
      return {
        'btn-warning': this.extension.enabled,
        'btn-success': !this.extension.enabled
      }
    },
    badges: function() {
      type Badges = {[key: string]: Array<string>};
      var badges:Badges = {};
      if(!this.extension.enabled) {
        badges.disabled = ["badge-warning"];
      }
      if(this.extension.builtin) {
        badges.builtin = ["badge-secondary"];
      }
      return badges;
    }
  },
  methods: {
    toggle: function() {
      const action = this.extension.enabled ? "disable" : "enable";
      alert("Cannot " + action + " '" + this.extension.human_name + "' plugin, because this function is not yet implemented :/");
    }
  },
  template: `
<div class="card">
  <div class="card-header d-flex flex-row align-items-center justify-content-between p-1 pr-4">
    <h5 :id="'heading' + name" class="my-auto">
      <button class="btn btn-link collapsed text-left" data-toggle="collapse" :data-target="'#collapse' + name" aria-expanded="false" :aria-controls="'collapse' + name">
        {{ extension.human_name }}
      </button>
    </h5>
    <div class="d-flex justify-content-end">
      <ul class="d-inline d-sm-flex nav nav-tabs card-header-tabs pull-right my-auto" role="tablist">
        <li class="nav-item text-right text-sm-left" v-for="(cls, name) in badges">
          <span :class="cls" class="ml-1 badge">{{ name }}</span>
        </li>
      </ul>
    </div>
  </div>
  <div :id="'collapse' + name" class="collapse" :aria-labelledby="'heading' + name" data-parent="#plugin-list-accordion">
    <ul class="list-group list-group-flush">
      <li class="list-group-item">
        <p>{{ extension.description }}</p>
        <p v-if="extension.author != null">Author: {{ extension.author }}</p>
        <p v-if="extension.url != null"><a :href="extension.url">{{ extension.url }}</a></p>
      </li>
    </ul>
    <div class="card-body">
      <form class="form form-inline pull-right">
        <div class="form-group">
          <button v-if="extension.disableable" @click="toggle" type="button" class="form-control btn" :class="disableClass" >{{ disableValue }}</button>
          <button v-else type="button" class="form-control btn disabled" :class="disableClass" disabled>{{ disableValue }}</button>
        </div>
      </form>
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
        type: "post",
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
