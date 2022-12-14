import { describe, it, beforeAll, vi, expect } from "vitest";
import { mount } from "@vue/test-utils";
import ViewInformationCard from "src/components/ViewInformationCard.vue";
import { application_config } from "src/test/CommonMock.js";
describe("Test Component ViewInformationCard", async () => {
  let propsMock;
  beforeAll(() => {
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
    it("should be called function getErrorGetFlagNotFound. when erro trying to load cardImg", async () => {
      const wrapper = mount(ViewInformationCard, {
        props: propsMock,
        global: { provide: { application_config } },
      });
      const cardImg = wrapper.find({ ref: "cardImg" });
      const spy = vi.spyOn(wrapper.vm, "getErrorGetFlagNotFound");
      await cardImg.trigger("error");
      expect(spy).toBeCalled();
    });

    it("should be called function getFlagUrl. when try to load cardImg", async () => {
      const wrapper = mount(ViewInformationCard, {
        props: propsMock,
        global: { provide: { application_config } },
      });
      const spy = vi.spyOn(wrapper.vm, "getFlagUrl");
      await wrapper.vm.$forceUpdate();
      expect(spy).toBeCalled();
    });
  });
});
