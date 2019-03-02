module.exports = {
  setupTestFrameworkScriptFile: '<rootDir>/tests/unit/jest-setup.js',
  moduleFileExtensions: [
    'js',
    'jsx',
    'json',
    'vue',
    'ts',
    'tsx'
  ],
  transform: {
    '^.+\\.vue$': 'vue-jest',
    '.+\\.(css|styl|less|sass|scss|svg|png|jpg|ttf|woff|woff2)$': 'jest-transform-stub',
    '^.+\\.jsx?$': 'babel-jest'
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  snapshotSerializers: [
    'jest-serializer-vue'
  ],
  testMatch: [
    '**/tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx)'
  ],
  testURL: 'http://localhost/',
  coverageReporters: [
    'json',
    'html',
    'text-summary'
  ],
  coverageDirectory: '<rootDir>/coverage',
  collectCoverageFrom: [
    'src/**/*.{ts,js,vue}',
    '!**/node_modules/**',
    '!tests/**',
    '!src/main.js',
    '!src/plugins/services/index.js',
    '!src/i18n.js',
    '!src/plugins/vuetify.js',
    '!src/store.js',
    '!src/router.js'
  ]
}
