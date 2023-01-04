import ViewInformation from "@/components/ViewInformation.vue";
import { shallowMount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  chartDataMock,
  resultMock,
  resultWithIndicatorsEmptyMock,
} from "../commonMock.js";

vi.mock("@/common/helpers.js");
describe("Test Component ViewInformation", () => {
  let propsMock;
  beforeEach(() => {
    propsMock = {
      countries: {
        country: [],
        indicators: [],
        idBase: "",
      },
    };
  });
  describe("Test ViewInformationCard loading", () => {
    it("should show ViewInformationCard when result.country is not empty", async () => {
      //Arrange
      const wrapper = shallowMount(ViewInformation, {
        props: propsMock,
      });

      //Act
      wrapper.vm.result = resultMock;
      await wrapper.vm.$forceUpdate();

      //Assert
      const viewInformationCard = wrapper.findComponent({
        ref: "viewInformationCard",
      });
      expect(viewInformationCard.exists()).toBeTruthy();
    });

    it("should not show ViewInformationCard when result.country is empty", async () => {
      //Arrange
      const wrapper = shallowMount(ViewInformation, {
        props: propsMock,
      });

      //Act
      wrapper.vm.result = [];
      await wrapper.vm.$forceUpdate();
      const viewInformationCard = wrapper.findComponent({
        ref: "viewInformationCard",
      });

      //Assert
      expect(viewInformationCard.exists()).toBeFalsy();
    });
  });

  describe("Test ViewInformationChart loading", () => {
    it("should not show ViewInformationChart when result.indicators is empty", async () => {
      //Arrange
      const wrapper = shallowMount(ViewInformation, {
        props: propsMock,
      });

      //Act
      wrapper.vm.result = resultWithIndicatorsEmptyMock;
      await wrapper.vm.$forceUpdate();
      const viewInformationChart = wrapper.findComponent({
        ref: "viewInformationChart",
      });

      //Assert
      expect(viewInformationChart.exists()).toBeFalsy();
    });

    it("should show ViewInformationChart when result.indicators and chartData are not empty", async () => {
      //Arrange
      const wrapper = shallowMount(ViewInformation, {
        props: propsMock,
      });

      //Act
      wrapper.vm.result = resultMock;
      await wrapper.vm.$forceUpdate();
      wrapper.vm.chartData = chartDataMock("");
      await wrapper.vm.$forceUpdate();
      const viewInformationChart = wrapper.findComponent({
        ref: "viewInformationChart",
      });

      //Assert
      expect(viewInformationChart.exists()).toBeTruthy();
    });
  });

  describe("Test scroll page", () => {
    let helpersMock;
    beforeEach(async () => {
      helpersMock = await import("@/common/helpers.js");
      helpersMock.scrollToId = vi.fn();
    });

    it("should call helpers.scrollToId when component updated", async () => {
      //Arrange
      const wrapper = shallowMount(ViewInformation, { props: propsMock });

      //Act
      await wrapper.vm.$forceUpdate();

      //Assert
      expect(helpersMock.scrollToId).toBeCalled();
    });

    it("should not call helpers.scrollToId when component not updated", () => {
      //Arrange
      shallowMount(ViewInformation, { props: propsMock });

      //Assert
      expect(helpersMock.scrollToId).not.toBeCalled();
    });
  });

  describe("Test ButtonComponent click", () => {
    it("should emit clickBtn when ButtonComponent were clicked", async () => {
      const wrapper = shallowMount(ViewInformation, { props: propsMock });

      wrapper.vm.result = resultMock;
      await wrapper.vm.$forceUpdate();
      const buttonComponent = wrapper.findComponent("#goBackButton");
      buttonComponent.trigger("click");
      await wrapper.vm.$nextTick();

      expect(wrapper.emitted()).toHaveProperty("clickBtn");
    });

    it("should not emit clickBtn when ButtonComponent is not clicked", async () => {
      const wrapper = shallowMount(ViewInformation, { props: propsMock });
      wrapper.vm.result = resultMock;

      await wrapper.vm.$forceUpdate();

      expect(wrapper.emitted()).not.toHaveProperty("clickBtn");
    });
  });
});
