import { describe, expect, it } from "vitest";
import { genChartsIndicator } from "/src/common/helpers.js";

/**
 * @description country mock
 * @return {import("../../src/common/helpers.js").Country} country
 */
function getCountryMock() {
  return [
    {
      id: "id",
      name: "name",
      capitalCity: "capitalCity",
      latitude: 0,
      longitude: 0,
      region: "region",
      incomeLevel: "incomeLevel",
      indicators: [
        {
          id: "id",
          description: "description",
          data: [
            {
              value: 0,
              year: 0,
            },
          ],
        },
      ],
    },
  ];
}
/**
 * @description mock ochart
 * @return {import("../../src/common/helpers.js").DataChart} datachart
 */
function getChartsIndicatorExpect() {
  return {
    id: {
      id: "id",
      description: "description",
      labels: ["0"],
      datasets: [
        { data: [0], label: "name", borderColor: "ANY_COLOR", fill: false },
      ],
      countryIds: new Set(["id"]),
    },
  };
}

/**
 * @description mock ochart
 * @param {import("../../src/common/helpers.js").DataChartDataset} dataset
 * @return {import("../../src/common/helpers.js").DataChartDataset} dataset with borderColor equals ANY_COLOR
 */
function removeBorderRandonColor(dataset) {
  return (dataset.borderColor = "ANY_COLOR");
}

describe("Test helpers", () => {
  it("should genChartsIndicator returns dataChart", () => {
    const countryMock = getCountryMock();
    const received = genChartsIndicator(countryMock);
    received.id.datasets.forEach(removeBorderRandonColor);
    const expected = getChartsIndicatorExpect();
    expect(expected).toEqual(received);
  });
});
