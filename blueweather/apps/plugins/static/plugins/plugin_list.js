var plugin_header = Vue.extend({
    props: {
        page: Number,
        pages: Number,
        page_size: Number
    },
    watch: {
        page_size: {
            immediate: true,
            handler: function (newVal, oldVal) {
                this.pageSize = newVal.toString();
            }
        },
        pageSize: function (newVal, oldVal) {
            if (newVal != this.page_size) {
                this.$emit('set-size', parseInt(newVal));
            }
        }
    },
    data: function () {
        return {
            pageSize: '10'
        };
    },
    computed: {
        page_numbers: function () {
            var n = 3;
            var start = Math.max(0, Math.floor(this.page - n / 2));
            var end = Math.min(this.pages, start + n);
            return _.range(start, end);
        }
    },
    methods: {
        activeClass: function (enabled) {
            if (enabled) {
                return [
                    'text-primary'
                ];
            }
            else {
                return [
                    'btn-primary'
                ];
            }
        },
        endsClass: function (enabled) {
            if (enabled) {
                return [
                    'text-primary'
                ];
            }
            else {
                return [
                    'text-secondary'
                ];
            }
        },
        enabled: function (index) {
            return index != this.page;
        },
        setPage: function (index) {
            this.$emit('set-page', index);
        }
    },
    template: "<form class=\"form-inline\" action=\"#\">\n  <div class=\"form-group mb-0 ml-sm-auto mr-auto mr-sm-0 mt-2 mt-sm-0\">\n    <select v-model=\"pageSize\" class=\"form-control\">\n      <option>1</option>\n      <option>2</option>\n      <option>4</option>\n      <option>5</option>\n      <option>10</option>\n      <option>25</option>\n      <option>50</option>\n      <option>100</option>\n    </select>\n  </div>\n  <div class=\"form-group mb-0 ml-3\">\n    <button role=\"button\" class=\"btn\"\n        :class=\"endsClass(enabled(0))\"\n        :disabled=\"!enabled(0)\"\n        @click=\"setPage(0)\">\n      <i class=\"fas fa-chevron-left\"></i>\n    </button>\n    <button v-for=\"i in page_numbers\" \n        :class=\"activeClass(enabled(i))\"\n        :disabled=\"!enabled(i)\"\n        @click=\"setPage(i)\"\n          role=\"button\" class=\"btn\">{{ i + 1 }}</button>\n    <button role=\"button\" class=\"btn\"\n        :class=\"endsClass(enabled(pages - 1))\"\n        :disabled=\"!enabled(pages - 1)\"\n        @click=\"setPage(pages - 1)\">\n      <i class=\"fas fa-chevron-right\"></i>\n    </button>\n  </div>\n</form>"
});
var plugin_item = Vue.extend({
    props: {
        plugin: Object,
    },
    computed: {
        badges: function () {
            var badges = [];
            if (this.plugin.builtin) {
                badges.push({
                    color: 'secondary',
                    value: 'builtin'
                });
            }
            if (!this.plugin.enabled) {
                badges.push({
                    color: 'warning',
                    value: 'disabled'
                });
            }
            return badges;
        },
        homepage: function () {
            if (this.plugin.info.homepage == null) {
                return null;
            }
            var url = new URL(this.plugin.info.homepage);
            return url.host;
        }
    },
    template: "<li class=\"list-group-item\">\n  <!-- Header -->\n  <div class=\"mb-2\">\n    <h4 class=\"d-inline mb-0\">{{ plugin.pluginName }}</h4>\n    <small v-if=\"plugin.pluginName != plugin.info.packageName\" class=\"d-inline\">\n    - {{ plugin.info.packageName }}\n    </small>\n\n    <!-- Badges -->\n    <div class=\"float-md-right\">\n      <span v-for=\"badge in badges\"\n          :class=\"'badge-' + badge.color\"\n          class=\"d-inline badge ml-2\">{{ badge.value }}</span>\n    </div>\n  </div>\n  <p v-if=\"plugin.info.summary\">{{ plugin.info.summary }}</p>\n\n  <!-- Footer -->\n  <div>\n    <small v-if=\"plugin.info.version\" \n        class=\"d-inline mr-2\">\n      <i class=\"fas fa-pen\"></i>\n      {{ plugin.info.version }}\n    </small>\n    <small v-if=\"plugin.info.homepage\"\n        class=\"d-inline mr-2\">\n      <i class=\"fas fa-home\"></i>\n      <a :href=\"plugin.info.homepage\" target=\"_blank\">{{ homepage }}</a>\n    </small>\n    <small v-if=\"plugin.info.author\"\n        class=\"d-inline mr-2\">\n      <i class=\"fas fa-address-book\"></i>\n      {{ plugin.info.author }}\n    </small>\n    <small v-if=\"plugin.info.license\"\n        class=\"d-inline\">\n      <i class=\"fas fa-file-contract\"></i>\n      {{ plugin.info.license }}\n    </small>\n  </div>\n</li>\n"
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
            pages: 1,
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
        getData: function () {
            var self = this;
            $.ajax({
                url: "/api/plugins/list",
                type: "get",
                data: {
                    page: self.page,
                    size: self.pageSize
                },
                success: function (data) {
                    self.plugins = data.plugins;
                    self.page = data.page;
                    self.pages = data.pages;
                }
            });
        },
        setPage: function (page) {
            this.page = page;
            this.getData();
        },
        setPageSize: function (size) {
            this.pageSize = size;
            this.getData();
        }
    }
});
