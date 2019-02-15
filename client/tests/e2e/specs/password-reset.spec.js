describe('/password-reset', () => {
  it('renders properties correctly', () => {
    cy.visit('#/password-reset')

    cy.get('p[data-ref=greeting-label]')
      .should('contain', 'Reset your password')
    cy.get('p[data-ref=app-name]')
      .should('contain', 'Cash Miner')
    cy.get('p[data-ref=help-text]')
      .should('contain', 'Enter your email address')
    cy.get('button[data-ref=submit] div:first')
      .should('contain', 'Send password reset email')
  })

  it('resets the form and focus on email field when api returns an error', () => {
    cy.visit('#/password-reset')

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
    cy.visit('#/password-reset')

    cy.get('form[data-ref=form]').within(() => {
      cy.get('button[data-ref=submit]')
        .click()
      cy.focused()
        .should('have.attr', 'data-ref', 'email')
        .should('have.value', '')
    })
  })

  it('hides the form and show the button to return to sig in when successfully submit', () => {
    cy.visit('#/password-reset')

    cy.get('form[data-ref=form]').within(() => {
      cy.get('input[data-ref=email]')
        .type('john.doe@test.com')
      cy.get('button[data-ref=submit]')
        .click()
    })

    cy.get('p[data-ref=help-text]')
      .should('contain', 'Check your email')
    cy.get('a[data-ref=return-to-sign-in]')
      .should('have.attr', 'href', '#/sign-in')
    cy.get('a[data-ref=return-to-sign-in] div:first')
      .should('contain', 'Return to sign in')
    cy.get('form[data-ref=form]')
      .should('not.exist')
  })
})
