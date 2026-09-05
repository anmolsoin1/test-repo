// Waits demo: cy.intercept + cy.wait('@alias') for network waits,
// explicit per-command timeouts, and should-callback polling.
describe("the-internet: dynamic loading (waits)", () => {
  it("waits for the page fetch via cy.intercept + cy.wait alias", () => {
    cy.intercept("GET", "/dynamic_loading/2").as("dynamicPage");
    cy.visit("/dynamic_loading/2");
    cy.wait("@dynamicPage").its("response.statusCode").should("eq", 200);
    // Element is rendered after DOM ready; explicit timeout overrides the
    // 10s default for this command only.
    cy.get("#start button", { timeout: 5000 }).should("be.visible").click();
    cy.get("#loading").should("be.visible");
  });

  it("waits for the dynamically rendered element with explicit timeout", () => {
    cy.visit("/dynamic_loading/2");
    cy.get("#start button").click();
    // The "Hello World!" div appears ~5s after the click; give it 15s.
    // Cypress retries this assertion until it passes or the timeout hits —
    // no hard sleeps needed (retry-ability).
    cy.get("#finish h4", { timeout: 15000 }).should("have.text", "Hello World!");
  });

  it("polls element state with a should callback after loading", () => {
    cy.visit("/dynamic_loading/2");
    cy.get("#start button").click();
    // Callback form: retries the whole body until all assertions pass.
    cy.get("#finish", { timeout: 15000 }).should(($finish) => {
      expect($finish).to.be.visible;
      expect($finish.text()).to.include("Hello World!");
    });
  });
});
