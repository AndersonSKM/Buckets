describe('/sign-in', () => {
  it('redirects to sign in view when acess the root url', () => {
    cy.visit('/')
    cy.url()
      .should('contain', '/sign-in')
  })

  it('redirects to sign in view when acess the home url', () => {
    cy.visit('/home')
    cy.url()
      .should('contain', '/sign-in')
  })

  it('redirects to sign in view when acess an invalid url', () => {
    cy.visit('/some/invalid-url')
    cy.url()
      .should('contain', '/sign-in')
  })

  it('renders properties correctly', () => {
    cy.visit('/sign-in')
    cy.get('p[data-ref=greeting-label]')
      .should('contain', 'Sign in')
    cy.get('a[data-ref=password-forgot]')
      .should('have.attr', 'href', '#/password-forgot')
  })

  it('resets the form and focus on email field after submit with wrong values', () => {
    cy.visit('/sign-in')

    cy.get('form[data-ref=form]').within(() => {
      cy.get('input[data-ref=email]')
        .type('test@test.com')
      cy.get('input[data-ref=password]')
        .type('asdlpl1pl2')
      cy.get('button[data-ref=submit]')
        .click()
      cy.url()
        .should('contain', '/sign-in')
      cy.focused()
        .should('have.attr', 'data-ref', 'email')
        .should('have.value', '')
      cy.get('input[data-ref=password]')
        .should('have.value', '')
      cy.get('ul[data-ref=error-list] li:first')
        .should('contain', 'Unable to log in with provided credentials')
    })
  })
})
