// https://docs.cypress.io/guides/guides/plugins-guide.html

module.exports = (on, config) => {
  return Object.assign({}, config, {
    fixturesFolder: 'fixtures',
    integrationFolder: 'specs',
    screenshotsFolder: 'screenshots',
    videosFolder: 'videos',
    supportFile: 'support/index.js'
  })
}
