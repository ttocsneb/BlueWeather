var plugin_list_component = Vue.extend({
    props: {
        extension: Object,
        name: String
    },
    computed: {
        disableValue: function () {
            return this.extension.enabled ? "Disable" : "Enable";
        },
        disableClass: function () {
            return {
                'btn-warning': this.extension.enabled,
                'btn-success': !this.extension.enabled
            };
        },
        badges: function () {
            var badges = {};
            if (!this.extension.enabled) {
                badges.disabled = ["badge-warning"];
            }
            if (this.extension.builtin) {
                badges.builtin = ["badge-secondary"];
            }
            return badges;
        }
    },
    methods: {
        toggle: function () {
            var action = this.extension.enabled ? "disable" : "enable";
            alert("Cannot " + action + " '" + this.extension.human_name + "' plugin, because this function is not yet implemented :/");
        }
    },
    template: "\n<div class=\"card\">\n  <div class=\"card-header d-flex flex-row align-items-center justify-content-between p-1 pr-4\">\n    <h5 :id=\"'heading' + name\" class=\"my-auto\">\n      <button class=\"btn btn-link collapsed text-left\" data-toggle=\"collapse\" :data-target=\"'#collapse' + name\" aria-expanded=\"false\" :aria-controls=\"'collapse' + name\">\n        {{ extension.human_name }}\n      </button>\n    </h5>\n    <div class=\"d-flex justify-content-end\">\n      <ul class=\"d-inline d-sm-flex nav nav-tabs card-header-tabs pull-right my-auto\" role=\"tablist\">\n        <li class=\"nav-item text-right text-sm-left\" v-for=\"(cls, name) in badges\">\n          <span :class=\"cls\" class=\"ml-1 badge\">{{ name }}</span>\n        </li>\n      </ul>\n    </div>\n  </div>\n  <div :id=\"'collapse' + name\" class=\"collapse\" :aria-labelledby=\"'heading' + name\" data-parent=\"#plugin-list-accordion\">\n    <ul class=\"list-group list-group-flush\">\n      <li class=\"list-group-item\">\n        <p>{{ extension.description }}</p>\n        <p v-if=\"extension.author != null\">Author: {{ extension.author }}</p>\n        <p v-if=\"extension.url != null\"><a :href=\"extension.url\">{{ extension.url }}</a></p>\n      </li>\n      <li v-if=\"extension.entrypoints.length > 0\" class=\"list-group-item\">\n        <h6>Entry Points</h6>\n        <ul>\n          <li v-for=\"point in extension.entrypoints\">\n            <h6>{{ point }}</h6>\n          </li>\n        </ul>\n      </li>\n    </ul>\n    <div class=\"card-body\">\n      <form class=\"form form-inline pull-right\">\n        <div class=\"form-group\">\n          <button v-if=\"extension.disableable\" @click=\"toggle\" type=\"button\" class=\"form-control btn\" :class=\"disableClass\" >{{ disableValue }}</button>\n          <button v-else type=\"button\" class=\"form-control btn disabled\" :class=\"disableClass\" disabled>{{ disableValue }}</button>\n        </div>\n      </form>\n    </div>\n  </div>\n</div>\n"
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
