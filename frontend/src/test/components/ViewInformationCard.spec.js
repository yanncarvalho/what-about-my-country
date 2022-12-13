import { describe, it, beforeAll, vi, expect } from "vitest";
import { shallowMount } from "@vue/test-utils";
import ViewInformationCard from "src/components/ViewInformationCard.vue";

describe("Test Component ViewInformationCard", () => {
  let propsMock;
  beforeAll(async () => {
    const baseValueMock = "Test";
    propsMock = {
      countryInfo: {
        id: baseValueMock,
        name: baseValueMock,
        capitalCity: baseValueMock,
        region: baseValueMock,
        incomeLevel: baseValueMock,
        latitude: baseValueMock,
        longitude: baseValueMock,
      },
    };
  });
  describe("Test flag image loading", () => {
    it("should be called function helpers. when erro trying to load cardImg", async () => {
      const wrapper = shallowMount(ViewInformationCard, {
        props: propsMock,
      });
      const cardImg = wrapper.find({ ref: "cardImg" });
      wrapper.vm.onErrorGetFlagNotFound = vi.fn();
      await cardImg.trigger("error");
      expect(wrapper.vm.onErrorGetFlagNotFound).toBeCalled();
    });
  });
});
