describe("End-to-End SPA tests", () => {
  const countries = ["Brazil", "Mexico"];
  beforeEach(() => {
    const apiUrl = "**/" + Cypress.env("BACKEND_COUNTRY_ROUTE");
    cy.intercept("POST", apiUrl).as("api");
    cy.visit("/");
    cy.wait(`@api`);
  });

  /**
   * @description add country in dataList option
   * @param {string} countryName country to be add
   */
  function addCountry(countryName) {
    const countryInput =
      "#datalistCountry > .tags-input-wrapper-default > input";
    const countryDropdownMenu =
      ".typeahead-dropdown > .tags-input-typeahead-item-highlighted-default";

    cy.get(countryInput).type(countryName);
    cy.get(countryDropdownMenu).click();
  }

  it("should show country information", () => {
    //Arrange
    const countryCard = (arrayIndex) =>
      `:nth-child(${arrayIndex + 1}) > .col > .card`;

    //Act
    addCountry(countries[0]);
    addCountry(countries[1]);
    cy.get("#showCountriesBtn").click();

    //Assert
    cy.get(countryCard(0)).contains(countries[0]);
    cy.get(countryCard(1)).contains(countries[1]);
  });

  it("should show chart", () => {
    //Arrange
    const chartFirstOption = ".tags-input-typeahead-item-highlighted-default";
    const chartView = "[id^=viewInformationChart] > #line-chart";

    //Act
    addCountry(countries[0]);
    cy.get(chartFirstOption).click();
    cy.get("#showCountriesBtn").click();

    //Assert
    cy.get(chartView).should("have.length", 1);
  });

  it("should showCountriesBtn be disabled after clicked", () => {
    //Arrange
    addCountry(countries[0]);

    //Act
    cy.get("#showCountriesBtn").click();

    //Assert
    cy.get("#showCountriesBtn").should("is.disabled");
  });
});
