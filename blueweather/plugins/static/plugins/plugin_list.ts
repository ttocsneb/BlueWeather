/// <reference types="vue" />
/// <reference types="jquery" />

interface PluginItem {
  human_name: string;
  description: string;
  author: string;
  url: string;
  entrypoints: Array<string>;
  builtin: boolean;
}
type PluginList = {[key: string]: PluginItem}

const plugin_list_component = Vue.extend({
  data: function name() {
    var extensions: PluginList = {};
    return {
      extensions: extensions
    };
  },
  beforeMount: function () {
    const _this = this;
    $.ajax("/api/plugins/list").done(function name(data:string) {
      _this.extensions = data;
    });
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
  components: {
    'plugin-list': plugin_list_component
  }
});
