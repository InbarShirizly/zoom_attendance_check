const webpack = require('webpack')
const path = require('path')
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin')

module.exports = {
  mode: process.env.NODE_ENV || 'development',
  devtool: 'inline-source-map',
  entry: {
    app: './src/app.tsx'
  },
  devServer: {
    contentBase: [
      path.resolve(__dirname, 'assets'),
      path.resolve(__dirname, 'dist')
    ]
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [{
      test: /\.tsx?$/,
      use: 'ts-loader',
      exclude: /node_modules/
    }]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],
  resolve: {
    plugins: [
      new TsconfigPathsPlugin()
    ],
    alias: {
      translations: path.resolve(__dirname, 'assets/translations')
    }
  }
}
