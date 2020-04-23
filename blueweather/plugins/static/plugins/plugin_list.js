var plugin_list_component = Vue.extend({
    props: {
        extensions: Object,
    },
    template: "\n<div id=\"plugin-list-accordion\">\n  <div class=\"card\" v-for=\"(ext, name) in extensions\">\n    <div class=\"card-header\">\n      <h5 class=\"mb-0\" :id=\"'heading' + name\">\n              <button class=\"btn btn-link collapsed\" data-toggle=\"collapse\" :data-target=\"'#collapse' + name\" aria-expanded=\"false\" :aria-controls=\"'collapse' + name\">\n                {{ ext.human_name }}\n                <span v-if=\"ext.builtin\" class=\"badge badge-secondary\">builtin</span>\n              </button>\n      </h5>\n    </div>\n    <div :id=\"'collapse' + name\" class=\"collapse\" :aria-labelledby=\"'heading' + name\" data-parent=\"#plugin-list-accordion\">\n      <ul class=\"list-group list-group-flush\">\n        <li class=\"list-group-item\">\n          <p>{{ ext.description }}</p>\n          <p v-if=\"ext.author != null\">Author: {{ ext.author }}</p>\n          <p v-if=\"ext.url != null\"><a :href=\"ext.url\">{{ ext.url }}</a></p>\n        </li>\n      </ul>\n      <div class=\"card-body\">\n        <h6>Entry Points</h6>\n        <ul>\n          <li v-for=\"point in ext.entrypoints\">\n            <h6>{{ point }}</h6>\n          </li>\n        </ul>\n      </div>\n    </div>\n  </div>\n</div>\n"
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
        };
    },
    components: {
        'plugin-list': plugin_list_component
    },
    beforeMount: function () {
        this.getData();
    },
    methods: {
        getData: function (page) {
            if (page === void 0) { page = 0; }
            var _this = this;
            $.ajax({
                url: "/api/plugins/list",
                type: "get",
                data: {
                    page: page,
                    items: _this.pageSize
                },
                success: function (data) {
                    _this.extensions = data.plugins;
                    _this.page = data.page;
                    _this.items = data.items;
                    _this.pages = data.pages;
                    _this.total = data.total;
                }
            });
        },
        first: function () {
            this.getData(0);
        },
        last: function () {
            this.getData(this.pages - 1);
        },
        next: function () {
            this.getData(Math.min(this.page + 1, this.pages - 1));
        },
        prev: function () {
            this.getData(Math.max(this.page - 1, 0));
        }
    },
    computed: {
        pageList: function () {
            var display = 5;
            var half = Math.floor(display / 2);
            var start = Math.min(Math.max(this.page - half, 0), this.page + half, Math.max(this.pages - display, 0));
            var size = Math.min(display, this.pages - start);
            return _.range(start, start + size);
        }
    }
});
