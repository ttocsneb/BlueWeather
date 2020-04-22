var plugin_list_component = Vue.extend({
    data: function name() {
        var extensions = {};
        return {
            extensions: extensions
        };
    },
    beforeMount: function () {
        var _this = this;
        $.ajax("/api/plugins/list").done(function name(data) {
            _this.extensions = data;
        });
    },
    template: "\n<div id=\"plugin-list-accordion\">\n  <div class=\"card\" v-for=\"(ext, name) in extensions\">\n    <div class=\"card-header\">\n      <h5 class=\"mb-0\" :id=\"'heading' + name\">\n              <button class=\"btn btn-link collapsed\" data-toggle=\"collapse\" :data-target=\"'#collapse' + name\" aria-expanded=\"false\" :aria-controls=\"'collapse' + name\">\n                {{ ext.human_name }}\n                <span v-if=\"ext.builtin\" class=\"badge badge-secondary\">builtin</span>\n              </button>\n      </h5>\n    </div>\n    <div :id=\"'collapse' + name\" class=\"collapse\" :aria-labelledby=\"'heading' + name\" data-parent=\"#plugin-list-accordion\">\n      <ul class=\"list-group list-group-flush\">\n        <li class=\"list-group-item\">\n          <p>{{ ext.description }}</p>\n          <p v-if=\"ext.author != null\">Author: {{ ext.author }}</p>\n          <p v-if=\"ext.url != null\"><a :href=\"ext.url\">{{ ext.url }}</a></p>\n        </li>\n      </ul>\n      <div class=\"card-body\">\n        <h6>Entry Points</h6>\n        <ul>\n          <li v-for=\"point in ext.entrypoints\">\n            <h6>{{ point }}</h6>\n          </li>\n        </ul>\n      </div>\n    </div>\n  </div>\n</div>\n"
});
var plugin_list = new Vue({
    el: '#plugin-list',
    components: {
        'plugin-list': plugin_list_component
    }
});
