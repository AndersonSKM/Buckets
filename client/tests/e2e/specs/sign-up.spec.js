describe('/sign-up', () => {
  beforeEach(() => {
    cy.visit('#/sign-up')
  })

  it('renders correctly', () => {
    cy.get('p[data-ref=greeting-label]')
      .should('contain', 'Sign up')
    cy.get('form[data-ref=form]')
      .should('be.visible')
    cy.get('div[data-ref=try-sign-in]')
      .should('not.exist')
    cy.get('div[data-ref=success-info]')
      .should('not.be.visible')
    cy.get('p[data-ref=sign-in-reference-label]')
      .should('contain', 'Already have an account?')
    cy.get('a[data-ref=sign-in-reference-link]')
      .should('have.attr', 'href', '#/sign-in')
  })

  it('resets the form and clear the password field after submit with wrong values', () => {
    cy.get('form[data-ref=form]').within(() => {
      cy.get('input[data-ref=name]')
        .type('Test User')
      cy.get('input[data-ref=email]')
        .type('test@test.com')
      cy.get('input[data-ref=password]')
        .type('test')
      cy.get('button[data-ref=submit]')
        .click()
    })

    cy.url()
      .should('contain', '#/sign-up')
    cy.get('input[data-ref=password]')
      .should('have.value', '')
    cy.get('div[data-ref=try-sign-in]')
      .should('not.exist')
    cy.get('div[data-ref=success-info]')
      .should('not.be.visible')
  })

  it('Display the alert when form is successfully submitted', () => {
    cy.seed({ create: false })

    cy.get('form[data-ref=form]').within(() => {
      cy.get('input[data-ref=name]')
        .type('John Doe')
      cy.get('input[data-ref=email]')
        .type('john.doe@test.com')
      cy.get('input[data-ref=password]')
        .type('aidj12j0dj10102')
      cy.get('button[data-ref=submit]')
        .click()
    })

    cy.url()
      .should('contain', '#/sign-up')
    cy.get('a[data-ref=return-to-sign-in] div:first')
      .should('contain', 'Sign in')
    cy.get('a[data-ref=return-to-sign-in]')
      .should('have.attr', 'href', '#/sign-in')
    cy.get('div[data-ref=success-info]')
      .should('be.visible')
      .should('contain', 'Please check your email and verify your email address.')
  })
})
