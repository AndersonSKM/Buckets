import './commands'

before(() => {
  cy.log('Seeding tests user')
  cy.seed({ create: true })
})
