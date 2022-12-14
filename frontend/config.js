export const config = {
  REFERENCE_SOURCE: {
    URL: "https://databank.worldbank.org/",
    NAME: "World Bank",
  },
  BACKEND: {
    COUNTRY_URL: "http://192.168.0.5:8080/api/v1/country",
  },
  FLAG: {
    NOT_FOUND: "src/assets/flag-not-found.png",
    REQUEST: {
      BASE_URL: "https://flagcdn.com/w640/",
      IMAGE_FORMAT: "webp",
    },
  },
  CHART: {
    NOT_FOUND_PATH: "src/assets/chart-not-found-data.png",
  },
  LOGO: {
    PATH: "src/assets/logo.svg",
  },
};
