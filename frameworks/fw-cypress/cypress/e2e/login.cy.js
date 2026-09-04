describe("the-internet: login page", () => {
  it("logs in with valid credentials and lands on /secure", () => {
    cy.visit("/login");
    cy.get("#username").type("tomsmith");
    cy.get("#password").type("SuperSecretPassword!");
    cy.get('button[type="submit"]').click();
    cy.url().should("include", "/secure");
    cy.get(".flash.success").should("contain", "You logged into a secure area!");
  });

  it("shows an error for invalid credentials", () => {
    cy.visit("/login");
    cy.get("#username").type("baduser");
    cy.get("#password").type("badpass");
    cy.get('button[type="submit"]').click();
    cy.get(".flash.error").should("contain", "Your username is invalid!");
  });
});
