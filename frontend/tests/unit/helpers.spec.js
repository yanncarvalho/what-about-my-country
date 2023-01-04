/* eslint-disable no-undef */
import { genChartsIndicator, genHexDecimalColor } from "@/common/helpers.js";
import { beforeEach, describe, expect, it } from "vitest";
import {
  chartDataMock,
  countryInfoMock as countryMock,
  indicatorsKeys as indiKeys,
} from "../commonMock.js";

describe("Test helpers", () => {
  let colorMock;
  beforeEach(() => {
    global.Math.random = () => 0.5;
    colorMock = "#7a11f8";
  });
  describe("Test genChartsIndicator", () => {
    it("should return dataChart", () => {
      //Arrange
      const received = genChartsIndicator([indiKeys], [countryMock]);
      const expected = chartDataMock(colorMock);

      //Assert
      expect(expected).toStrictEqual(received);
    });
  });
  describe("Test genChartsIndicator", () => {
    it("should return a valid color", () => {
      //Arrange
      const hexDecimalColor = genHexDecimalColor();

      //Assert
      expect(hexDecimalColor).toBe(colorMock);
    });
  });
});
