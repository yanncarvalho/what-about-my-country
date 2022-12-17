import { shallowMount } from "@vue/test-utils";
import ViewInformationChart from "src/components/ViewInformationChart.vue";
import { beforeEach, describe, expect, it, vi } from "vitest";

describe("Test Component ViewInformationChart", () => {
  let propsMock;
  beforeEach(() => {
    global.__APP_ENV__ = vi.fn();
    propsMock = {
      labels: [],
      datasets: [],
      description: "",
      countriesWithoutData: [],
      id: "id",
    };
  });
  describe("Test notFoundImg loading", () => {
    it("should show notFoundImg when props.datasets is empty", () => {
      //Arrange
      propsMock.datasets = [];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
      });

      //Assert
      expect(wrapper.find({ ref: "notFoundImg" }).exists()).toBeTruthy();
    });

    it("should not show notFoundImg when props.datasets is not empty", () => {
      //Arrange
      propsMock.datasets = ["ANY_VALUE"];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
      });

      //Assert
      expect(wrapper.find({ ref: "notFoundImg" }).exists()).toBeFalsy();
    });
  });

  describe("Test chart loading", () => {
    it("should show chart when props.datasets is not empty", () => {
      //Arrange
      propsMock.datasets = ["ANY_VALUE"];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
      });

      //Assert
      expect(wrapper.findComponent({ ref: "chart" }).exists()).toBeTruthy();
    });

    it("should not show chart when props.datasets is empty", () => {
      //Arrange
      propsMock.datasets = [];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
      });

      //Assert
      expect(wrapper.findComponent({ ref: "chart" }).exists()).toBeFalsy();
    });
  });
});
