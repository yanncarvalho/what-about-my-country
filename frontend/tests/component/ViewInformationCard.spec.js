import ViewInformationCard from "@/components/ViewInformationCard.vue";
import { mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { countryInfoMock } from "../commonMock.js";

describe("Test Component ViewInformationCard", () => {
  let propsMock;
  beforeEach(() => {
    global.__APP_ENV__ = vi.fn();
    propsMock = {
      countryInfo: countryInfoMock,
      idBase: "",
    };
  });

  describe("Test flag image loading", () => {
    it("should call function getErrorGetFlagNotFound when erro trying to load cardImg", async () => {
      //Arrange
      const wrapper = mount(ViewInformationCard, {
        props: propsMock,
      });
      const cardImg = wrapper.find({ ref: "cardImg" });

      //Act
      const spy = vi.spyOn(wrapper.vm, "getErrorGetFlagNotFound");
      await cardImg.trigger("error");

      //Assert
      expect(spy).toBeCalled();
    });

    it("should call function getFlagUrl when try to load cardImg", async () => {
      //Arrange
      const wrapper = mount(ViewInformationCard, {
        props: propsMock,
      });

      //Act
      const spy = vi.spyOn(wrapper.vm, "getFlagUrl");
      await wrapper.vm.$forceUpdate();

      //Assert
      expect(spy).toBeCalled();
    });
  });
});
