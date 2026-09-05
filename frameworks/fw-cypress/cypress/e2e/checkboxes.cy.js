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

  it("polls checkbox count with a should callback (retry-ability)", () => {
    cy.visit("/checkboxes");
    // should() with a callback re-runs until every inner assertion passes
    // or the command timeout expires — Cypress's built-in retry-ability.
    cy.get("#checkboxes input").should(($inputs) => {
      expect($inputs).to.have.length(2);
      expect($inputs.eq(1)).to.be.checked; // second box is checked by default
    });
  });
});

describe("DELIBERATE FAILURE — expected to fail", () => {
  it("DELIBERATE_FAILURE asserts a heading that does not exist", () => {
    cy.visit("/checkboxes");
    // Deliberately wrong assertion to demonstrate a failing test row in the UI.
    cy.get("h3").should("have.text", "This heading text is intentionally wrong");
  });
});
