describe("the-internet: checkboxes", () => {
  it("checks and unchecks both checkboxes", () => {
    cy.visit("/checkboxes");
    cy.get("#checkboxes input").eq(0).check().should("be.checked");
    cy.get("#checkboxes input").eq(1).uncheck().should("not.be.checked");
  });

  it("checkbox state persists within the page session", () => {
    cy.visit("/checkboxes");
    cy.get("#checkboxes input").eq(0).check();
    cy.get("#checkboxes input").eq(0).should("be.checked");
  });
});

describe("DELIBERATE FAILURE — expected to fail", () => {
  it("DELIBERATE_FAILURE asserts a heading that does not exist", () => {
    cy.visit("/checkboxes");
    // Deliberately wrong assertion to demonstrate a failing test row in the UI.
    cy.get("h3").should("have.text", "This heading text is intentionally wrong");
  });
});
