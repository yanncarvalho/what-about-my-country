import { shallowMount } from "@vue/test-utils";
import App from "src/App.vue";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { application_config } from "../commonMock.js";

vi.mock("/src/common/helpers.js");
describe("Test Component App", () => {
  let onResultMock;
  beforeEach(async () => {
    onResultMock = {
      country: [{ key: "key", value: "value" }],
      indicator: [{ key: "key", value: "value" }],
    };
  });

  describe("Test requestInformation when emit onResult", () => {
    it("should change formResult when onResult emit", async () => {
      const wrapper = shallowMount(App, {
        global: { provide: { application_config } },
      });
      const requestInformation = wrapper.findComponent("#requestInformation");
      requestInformation.vm.$emit("onResult", onResultMock);
      await wrapper.vm.$forceUpdate();
      expect(wrapper.vm.formResult).toEqual(onResultMock);
    });
  });

  describe("Test ViewInformation when emit onResult", () => {
    it("should show when onResult.country is not empty", async () => {
      const wrapper = shallowMount(App, {
        global: { provide: { application_config } },
      });
      wrapper.vm.formResult = onResultMock;
      await wrapper.vm.$forceUpdate();
      const viewInformation = wrapper.findComponent({ ref: "viewInformation" });
      expect(viewInformation.exists()).toBeTruthy();
    });

    it("should not show when formResult.country is empty", async () => {
      const wrapper = shallowMount(App, {
        global: { provide: { application_config } },
      });
      onResultMock.country = [];
      wrapper.vm.formResult = onResultMock;
      await wrapper.vm.$forceUpdate();
      const viewInformation = wrapper.findComponent({ ref: "viewInformation" });
      expect(viewInformation.exists()).toBeFalsy();
    });
  });
});
