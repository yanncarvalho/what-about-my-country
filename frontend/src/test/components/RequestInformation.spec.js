import { describe, it, expect } from "vitest";
import { shallowMount } from "@vue/test-utils";
import RequestInformation from "src/components/RequestInformation.vue";

describe("Test Component RequestInformation", () => {
  /**
   * @description find ButtonComponent
   * @param {RequestInformation} parent RequestInformation where will be found
   * @returns {ButtonComponent} ButtonComponent
   */
  function createButtonComponent(parent) {
    return parent.findComponent({
      ref: "showCountriesBtn",
    });
  }

  describe("Test event when ButtonComponent is clicked", () => {
    it("should emit onResult event when ButtonComponent is clicked", async () => {
      const wrapper = shallowMount(RequestInformation);
      const ButtonComponent = createButtonComponent(wrapper);
      ButtonComponent.trigger("click");
      await wrapper.vm.$nextTick();
      expect(wrapper.emitted()).toHaveProperty("onResult");
    });

    it("should not emit onResult event until ButtonComponent is not clicked", async () => {
      const wrapper = shallowMount(RequestInformation);
      expect(wrapper.emitted()).not.toHaveProperty("onResult");
    });
  });

  describe("Test when ButtonComponent is disabled", () => {
    it("should be enabled when selectedTags.country is not empty and ButtonComponent has not click", async () => {
      const wrapper = shallowMount(RequestInformation);
      const ButtonComponent = createButtonComponent(wrapper);
      wrapper.vm.selectedTags.country = ["ANY VALUE"];
      await ButtonComponent.vm.$nextTick();
      expect(ButtonComponent.vm.disabled).toBeFalsy();
    });

    it("should be disabled when selectedTags.country is emmpty", async () => {
      const wrapper = shallowMount(RequestInformation);
      const ButtonComponent = createButtonComponent(wrapper);
      wrapper.vm.selectedTags.country = [];
      await ButtonComponent.vm.$nextTick();
      expect(ButtonComponent.vm.disabled).toBeTruthy();
    });

    it("should be disabled when has been clicked and selectedTags has not changed", async () => {
      const wrapper = shallowMount(RequestInformation);
      const ButtonComponent = createButtonComponent(wrapper);
      wrapper.vm.selectedTags.country = ["ANY_VALUE"];
      await wrapper.vm.$nextTick();
      ButtonComponent.trigger("click");
      await ButtonComponent.vm.$nextTick();
      expect(ButtonComponent.vm.disabled).toBeTruthy();
    });

    it("should be enabled when has been clicked and selectedTags has changed", async () => {
      const wrapper = shallowMount(RequestInformation);
      const ButtonComponent = createButtonComponent(wrapper);
      wrapper.vm.selectedTags.country = ["ANY_VALUE"];
      await wrapper.vm.$nextTick();
      ButtonComponent.trigger("click");
      await ButtonComponent.vm.$nextTick();
      expect(ButtonComponent.vm.disabled).toBeTruthy();
      wrapper.vm.selectedTags.indicator = ["NEW_VALUE"];
      await wrapper.vm.$nextTick();
      expect(ButtonComponent.vm.disabled).toBeFalsy();
    });
  });
});
