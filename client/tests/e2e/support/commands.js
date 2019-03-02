Cypress.Commands.add('seed', ({ create }) => {
  cy.request({
    method: 'POST',
    url: 'api/seed/',
    body: {
      create
    }
  })
})
