const path = require("path");

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
        use: "svelte-loader"
      }
    ]
  }
};
