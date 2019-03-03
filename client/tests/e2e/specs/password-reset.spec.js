describe('/password-reset', () => {
  beforeEach(() => {
    cy.visit('#/password-reset')
  })

  it('renders properties correctly', () => {
    cy.get('p[data-ref=greeting-label]')
      .should('contain', 'Reset your password')
    cy.get('p[data-ref=app-name]')
      .should('contain', 'Cash Miner')
    cy.get('p[data-ref=help-text]')
      .should('contain', 'Enter your email address')
    cy.get('button[data-ref=submit] div:first')
      .should('contain', 'Send password reset email')
    cy.get('div[data-ref=success-info]')
      .should('not.be.visible')
    cy.get('a[data-ref=try-sign-in]')
      .should('not.exist')
    cy.get('p[data-ref=sign-in-reference-label]')
      .should('contain', 'Remember your password?')
    cy.get('a[data-ref=sign-in-reference-link]')
      .should('have.attr', 'href', '#/sign-in')
  })

  it('resets the form and focus on email field when api returns an error', () => {
    cy.get('form[data-ref=form]').within(() => {
      cy.get('input[data-ref=email]')
        .type('test@test.com')
      cy.get('button[data-ref=submit]')
        .click()
      cy.focused()
        .should('have.attr', 'data-ref', 'email')
        .should('have.value', '')
    })
  })

  it('focus on email field when form is blank', () => {
    cy.get('form[data-ref=form]').within(() => {
      cy.get('button[data-ref=submit]')
        .click()
      cy.focused()
        .should('have.attr', 'data-ref', 'email')
        .should('have.value', '')
    })
  })

  it('hides the form and show the button to return to sign in when successfully submit', () => {
    cy.get('form[data-ref=form]').within(() => {
      cy.get('input[data-ref=email]')
        .type('john.doe@test.com')
      cy.get('button[data-ref=submit]')
        .click()
    })

    cy.get('div[data-ref=success-info]')
      .should('contain', 'Check your email')
    cy.get('a[data-ref=return-to-sign-in]')
      .should('have.attr', 'href', '#/sign-in')
    cy.get('a[data-ref=return-to-sign-in] div:first')
      .should('contain', 'Sign in')
    cy.get('form[data-ref=form]')
      .should('not.exist')
  })
})
