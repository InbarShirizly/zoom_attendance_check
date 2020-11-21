const webpack = require('webpack')
const path = require('path')
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin')
const packages = path.resolve(__dirname, 'packages')
const application = path.join(packages, 'application')

module.exports = {
  mode: process.env.NODE_ENV || 'development',
  devtool: 'inline-source-map',
  entry: {
    app: path.join(application, 'src', 'app.tsx')
  },
  devServer: {
    contentBase: [
      path.join(application, 'assets'),
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
      use: {
        loader: 'ts-loader',
        options: { projectReferences: true }
      },
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
      translations: path.join(application, 'assets', 'translations')
    }
  }
}
