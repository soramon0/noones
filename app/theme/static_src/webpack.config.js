const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");

const mode = process.env.NODE_ENV || "development";
const prod = mode === "production";

module.exports = {
  entry: {
    main: "./src/main/index.js",
    svelte: "./src/svelte/index.js"
  },
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "..", "static", "js")
  },
  resolve: {
    alias: {
      svelte: path.resolve("node_modules", "svelte")
    },
    extensions: [".mjs", ".js", ".svelte"],
    mainFields: ["svelte", "browser", "module", "main"]
  },
  module: {
    rules: [
      {
        test: /\.(html|svelte)$/,
        exclude: /node_modules/,
        use: {
          loader: "svelte-loader",
          options: {
            emitCss: true,
            hotReload: true
          }
        }
      },
      {
        test: /\.css$/,
        use: [prod ? MiniCssExtractPlugin.loader : "style-loader", "css-loader"]
      }
    ]
  },
  mode,
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css"
    })
  ],
  devtool: prod ? false : "source-map"
};
