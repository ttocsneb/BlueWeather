var plugin_header = Vue.extend({
    props: {
        page: Number,
        pages: Number,
        pageSize: Number
    },
    template: "<p><p>"
});
var plugin_item = Vue.extend({
    props: {
        plugin: Object,
    },
    template: "<li class=\"list-group-item\">\n  <h3>{{ plugin.name }}</h3>\n  <p v-if=\"plugin.info.summary\">{{ plugin.info.summary }}</p>\n  <ul>\n    <li v-if=\"plugin.info.version\">Version: {{ plugin.info.version }}</li>\n    <li v-if=\"plugin.info.homepage\">homepage: {{ plugin.info.homepage }}</li>\n    <li v-if=\"plugin.info.author\">author: {{ plugin.info.author }}</li>\n    <li v-if=\"plugin.info.email\">email: {{ plugin.info.email }}</li>\n    <li v-if=\"plugin.info.license\">license: {{ plugin.info.license }}</li>\n  </ul>\n</li>\n"
});
var plugin_body = Vue.extend({
    props: {
        plugins: Array
    },
    components: {
        'plugin-item': plugin_item
    },
    template: "<ul class=\"list-group list-group-flush\">\n  <plugin-item :plugin=\"plugin\" \n      v-for=\"plugin in plugins\" />\n</ul>\n"
});
var plugin_list = new Vue({
    el: '#plugin-list',
    data: function () {
        return {
            plugins: {},
            pages: 0,
            page: 0,
            pageSize: 10
        };
    },
    components: {
        'plugin-header': plugin_header,
        'plugin-body': plugin_body
    },
    beforeMount: function () {
        this.getData();
    },
    methods: {
        getData: function (page) {
            if (page === void 0) { page = 0; }
            var self = this;
            $.ajax({
                url: "/api/plugins/list",
                type: "get",
                data: {
                    page: page,
                    items: self.pageSize
                },
                success: function (data) {
                    self.plugins = data.plugins;
                    self.page = data.page;
                    self.pages = data.pages;
                    console.log(data);
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
