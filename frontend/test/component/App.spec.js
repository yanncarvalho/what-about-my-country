/* eslint-disable no-undef */
import { shallowMount } from "@vue/test-utils";
import App from "src/App.vue";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("/src/common/helpers.js");
describe("Test Component App", () => {
  let onResultMock;
  beforeEach(async () => {
    global.__APP_ENV__ = vi.fn();
    onResultMock = {
      country: [{ key: "key", value: "value" }],
      indicator: [{ key: "key", value: "value" }],
    };
  });

  describe("Test requestInformation when emit onResult", () => {
    it("should change formResult when onResult emitted", async () => {
      //Arrange
      const wrapper = shallowMount(App);
      const requestInformation = wrapper.findComponent("#requestInformation");

      //Act
      requestInformation.vm.$emit("onResult", onResultMock);
      await wrapper.vm.$forceUpdate();

      //Assert
      expect(wrapper.vm.formResult).toEqual(onResultMock);
    });
  });

  describe("Test ViewInformation when emit onResult", () => {
    it("should show when onResult.country is not empty", async () => {
      //Arrange
      const wrapper = shallowMount(App);

      //Act
      wrapper.vm.formResult = onResultMock;
      await wrapper.vm.$forceUpdate();

      //Assert
      const viewInformation = wrapper.findComponent({ ref: "viewInformation" });
      expect(viewInformation.exists()).toBeTruthy();
    });

    it("should not show when formResult.country is empty", async () => {
      //Arrange
      const wrapper = shallowMount(App);

      //Act
      onResultMock.country = [];
      wrapper.vm.formResult = onResultMock;
      await wrapper.vm.$forceUpdate();

      //Assert
      const viewInformation = wrapper.findComponent({ ref: "viewInformation" });
      expect(viewInformation.exists()).toBeFalsy();
    });
  });
});
