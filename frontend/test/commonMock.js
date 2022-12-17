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

export const chartDataMock = (borderColor) => {
  return {
    id: {
      id: "id",
      description: "description",
      labels: ["0"],
      datasets: [
        { data: [0], label: "name", borderColor: borderColor, fill: false },
      ],
      countryIds: new Set(["id"]),
    },
  };
};
