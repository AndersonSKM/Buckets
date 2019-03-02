module.exports = {
  outputDir: './../api/public/',
  assetsDir: 'static',
  devServer: {
    hot: true,
    progress: true,
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '/api/*': {
        target: 'http://localhost:8000',
        secure: false
      }
    }
  },
  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'pt-BR',
      localeDir: 'locales',
      enableInSFC: false
    }
  }
}
