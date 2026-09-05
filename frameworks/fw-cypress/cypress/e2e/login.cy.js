// Locator variety demo: css id, attribute selector, cy.contains by text,
// and cy.xpath (via cypress-xpath, registered in cypress/support/e2e.js).
// Note: the-internet.herokuapp.com has NO data-cy attributes, so the
// data-attribute pattern is demonstrated with the [name="..."] attribute
// selector, which is the same cy.get('[attr="value"]') mechanism.
describe("the-internet: login page (locator variety)", () => {
  beforeEach(() => {
    cy.visit("/login");
  });

  it("logs in with valid credentials and lands on /secure (css id selectors)", () => {
    cy.get("#username").type("tomsmith");
    cy.get("#password").type("SuperSecretPassword!");
    cy.get('button[type="submit"]').click();
    cy.url().should("include", "/secure");
    cy.get(".flash.success").should("contain", "You logged into a secure area!");
  });

  it("shows an error for invalid credentials (attribute selectors, data-cy pattern)", () => {
    // Same selector mechanism as [data-cy="username"] — the site just uses
    // name attributes instead.
    cy.get('[name="username"]').type("baduser");
    cy.get('[name="password"]').type("badpass");
    // cy.contains locates the submit button by its visible text.
    cy.contains("button", "Login").click();
    cy.get(".flash.error").should("contain", "Your username is invalid!");
  });

  it("finds the submit button via xpath (cypress-xpath)", () => {
    cy.xpath('//input[@id="username"]').type("tomsmith");
    cy.xpath('//input[@id="password"]').type("SuperSecretPassword!");
    cy.xpath('//button[@type="submit"]')
      .should("contain.text", "Login") // button text has a leading space (icon)
      .click();
    cy.xpath('//div[contains(@class,"flash success")]').should(
      "contain",
      "You logged into a secure area!"
    );
  });
});
