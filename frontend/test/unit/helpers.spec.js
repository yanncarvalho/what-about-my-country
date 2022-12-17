/* eslint-disable no-undef */
import { describe, expect, it, beforeEach } from "vitest";
import { genChartsIndicator, genHexDecimalColor } from "/src/common/helpers.js";
import {
  chartDataMock,
  countryInfoMock as countryMock,
} from "../commonMock.js";

describe("Test helpers", () => {
  let colorMock;
  beforeEach(() => {
    vi.spyOn(global.Math, "random").mockReturnValue(0.5);
    colorMock = "#7a11f8";
  });
  describe("Test genChartsIndicator", () => {
    it("should return dataChart", () => {
      //Arrange
      const received = genChartsIndicator([countryMock]);
      const expected = chartDataMock(colorMock);

      //Assert
      expect(expected).toEqual(received);
    });
  });
  describe("Test genChartsIndicator", () => {
    it("should return a valid color", () => {
      //Arrange
      const hexDecimalColor = genHexDecimalColor();

      //Assert
      expect(hexDecimalColor).toEqual(colorMock);
    });
  });
});
