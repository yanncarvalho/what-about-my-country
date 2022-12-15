export const application_config = {
  REFERENCE_SOURCE: {
    URL: "URL",
    NAME: "NAME",
  },
  BACKEND: {
    COUNTRY_URL: "COUNTRY_URL",
  },
  FLAG: {
    NOT_FOUND: "NOT_FOUND",
    REQUEST: {
      BASE_URL: "BASE_URL",
      IMAGE_FORMAT: "IMAGE_FORMAT",
    },
  },
  CHART: {
    NOT_FOUND_PATH: "NOT_FOUND_PATH",
  },
  LOGO: {
    PATH: "PATH",
  },
};

export const indicatorsMock = {
  id: "id",
  description: "description",
  data: [
    {
      value: 0,
      year: 0,
    },
  ],
};

export const countryInfoMock = {
  id: "id",
  name: "name",
  capitalCity: "capitalCity",
  latitude: 0.0,
  longitude: 0.0,
  region: "region",
  incomeLevel: "incomeLevel",
  indicators: [indicatorsMock],
};
export const countryInfoWithIndicatorsEmptyMock = {
  id: "id",
  name: "name",
  capitalCity: "capitalCity",
  latitude: 0.0,
  longitude: 0.0,
  region: "region",
  incomeLevel: "incomeLevel",
  indicators: [],
};

export const resultWithIndicatorsEmptyMock = {
  country: [countryInfoWithIndicatorsEmptyMock],
};

export const resultMock = {
  country: [countryInfoMock],
};

export const chartDataMock = {
  id: {
    id: "id",
    description: "description",
    labels: ["label"],
    datasets: [
      {
        data: [0],
        label: "label",
        borderColor: "borderColor",
        fill: false,
      },
    ],
    countryIds: new Set(["countryIds"]),
  },
};
