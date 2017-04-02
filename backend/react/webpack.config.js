var path = require('path');
var webpack = require('webpack');
var HTMLWebpackPlugin = require('html-webpack-plugin');

const DEVELOPMENT = process.env.NODE_ENV === 'development';
const PRODUCTION = process.env.NODE_ENV === 'production';

const entry = PRODUCTION
    ? ['./src/root.js']
    : [
        './src/root.js',
        'webpack/hot/dev-server',
        'webpack-dev-server/client?http://localhost:8080'
      ];

const plugins = PRODUCTION
              ? [
                      new webpack.optimize.UglifyJsPlugin(),
                    new HTMLWebpackPlugin({
                        template: 'index-template.html'
                    })
                ]
              : [new  webpack.HotModuleReplacementPlugin()];
plugins.push(
    new webpack.DefinePlugin({
        DEVELOPMENT: JSON.stringify(DEVELOPMENT),
        PRODUCTION: JSON.stringify(PRODUCTION)
    })
);
module.exports = {
    devtool: 'source-map',
    entry: entry,
    plugins: plugins,
    module: {
        loaders: [{
            test: '/\.js$/',
            loaders: ['babel-loader'],
            exclude: '/node_modules/'
        }]
    },
    output: {
        path: path.join(__dirname, 'dist'),
        publicPath: PRODUCTION ? '/' : '/dist/',
        filename: PRODUCTION ? 'bundle.[hash:12].min.js' : 'bundle.js'
    }
};