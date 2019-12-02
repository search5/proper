module.exports = {
  'transpileDependencies': [
    'vuetify'
  ],
  devServer: {
    proxy: { // proxyTable 설정
      '/api': {
        target: 'http://localhost:5000',
        publicPath: {
          '^/api': ''
        }
      }
    }
  }
}
