const isProduction = process.env.NODE_ENV === "production";

module.exports = {
  publicPath: isProduction ? "/" : "http://127.0.0.1:8080",
  outputDir: isProduction ? "./dist" : "../static/dist",
  indexPath: isProduction ? "../templates/index.html" : "../../templates/index.html",

  pages: {
    index: {
      entry: "src/main.js",
      title: "Robot DB",
      template: isProduction ? 'public/index-prod.html' : 'public/index-dev.html',
    },
  },
  devServer: {
    devMiddleware: {
      publicPath: "http://127.0.0.1:8080",
      writeToDisk: (filePath) => !isProduction && filePath.endsWith("index.html"),
    },
    hot: "only",
    headers: { "Access-Control-Allow-Origin": "*" },
  },
};


