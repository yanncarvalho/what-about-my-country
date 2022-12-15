import { shallowMount } from "@vue/test-utils";
import ViewInformationChart from "src/components/ViewInformationChart.vue";
import { beforeEach, describe, expect, it } from "vitest";
import { application_config } from "../commonMock.js";

describe("Test Component ViewInformationChart", () => {
  let propsMock;
  beforeEach(() => {
    propsMock = {
      labels: [],
      datasets: [],
      description: "",
      countriesWithoutData: [],
    };
  });
  describe("Test notFoundImg loading", () => {
    it("should show notFoundImg when props.datasets is empty", () => {
      propsMock.datasets = [];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
        global: { provide: { application_config } },
      });
      expect(wrapper.find({ ref: "notFoundImg" }).exists()).toBeTruthy();
    });

    it("should not show notFoundImg when props.datasets is not empty", () => {
      propsMock.datasets = ["ANY_VALUE"];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
        global: { provide: { application_config } },
      });
      expect(wrapper.find({ ref: "notFoundImg" }).exists()).toBeFalsy();
    });
  });

  describe("Test chart loading", () => {
    it("should show chart when props.datasets is not empty", () => {
      propsMock.datasets = ["ANY_VALUE"];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
        global: { provide: { application_config } },
      });
      expect(wrapper.findComponent({ ref: "chart" }).exists()).toBeTruthy();
    });

    it("should not show chart when props.datasets is empty", () => {
      propsMock.datasets = [];
      const wrapper = shallowMount(ViewInformationChart, {
        props: propsMock,
        global: { provide: { application_config } },
      });
      expect(wrapper.findComponent({ ref: "chart" }).exists()).toBeFalsy();
    });
  });
});
