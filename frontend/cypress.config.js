/* eslint-disable no-undef */
const { defineConfig } = require("cypress");
require("dotenv").config();
module.exports = defineConfig({
  env: {
    BACKEND_COUNTRY_ROUTE: process.env.BACKEND_COUNTRY_ROUTE,
  },

  e2e: {
    specPattern: "test/e2e/*.cy.{js,jsx,ts,tsx}",
    baseUrl: `${process.env.FRONTEND_PROTOCOL}://${process.env.FRONTEND_ADRESS}:${process.env.FRONTEND_PORT}`,
  },
});
