var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader', query: {  presets:['react']}}, // to transform JSX into JS
    ],
  },

  resolve: {
    extensions: ['.js', '.jsx']
  },
}
