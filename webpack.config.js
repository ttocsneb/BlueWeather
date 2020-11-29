const path = require("path")
const VueLoaderPlugin = require("vue-loader/lib/plugin")

const exclude = [/node_modules/]
const publicPath = '/static/'
const outputDir = 'dist'

module.exports = {
    mode: "development",
    entry: {
        index: path.resolve(__dirname, "frontend/src/index.ts")
    },
    output: {
        path: path.resolve(__dirname, outputDir),
        filename: "[name].bundle.js",
        publicPath,
        library: "blueweather",
        libraryTarget: "umd"
    },
    module: {
        rules: [
            {
                test: /\.(t|j)s$/,
                loader: "ts-loader",
                exclude,
                options: {
                    appendTsSuffixTo: [/\.vue$/]
                }
            },
            {
                test: /\.vue$/,
                loader: "vue-loader",
                exclude
            }
        ]
    },
    resolve: {
        modules: [
            path.resolve(__dirname, "node_modules")
        ],
        extensions: [".js", ".ts", ".vue"],
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    devtool: "inline-source-map",
    target: "web",
    plugins: [
        new VueLoaderPlugin()
    ]
}
