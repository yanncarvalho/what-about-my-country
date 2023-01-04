import RequestInformation from "@/components/RequestInformation.vue";
import { shallowMount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

describe("Test Component RequestInformation", () => {
  /**
   * @description find ButtonComponent
   * @param {RequestInformation} parent RequestInformation where will be found
   * @returns {ButtonComponent} buttonComponent
   */
  function createButtonComponent(parent) {
    return parent.findComponent("#showCountriesBtn");
  }

  describe("Test event when ButtonComponent is clicked", () => {
    it("should emit onResult event when ButtonComponent is clicked", async () => {
      //Arrange
      const wrapper = shallowMount(RequestInformation);
      const buttonComponent = createButtonComponent(wrapper);

      //Act
      buttonComponent.trigger("click");
      await wrapper.vm.$nextTick();

      //Assert
      expect(wrapper.emitted()).toHaveProperty("onResult");
    });

    it("should not emit onResult event until ButtonComponent is not clicked", () => {
      //Arrange
      const wrapper = shallowMount(RequestInformation);

      //Assert
      expect(wrapper.emitted()).not.toHaveProperty("onResult");
    });
  });

  describe("Test when ButtonComponent is disabled", () => {
    it("should be enabled when selectedTags.country is not empty and ButtonComponent were not clicked", async () => {
      //Arrange
      const wrapper = shallowMount(RequestInformation);
      const buttonComponent = createButtonComponent(wrapper);

      //Act
      wrapper.vm.selectedTags.country = ["ANY VALUE"];
      await buttonComponent.vm.$nextTick();

      //Assert
      expect(buttonComponent.vm.disabled).toBeFalsy();
    });

    it("should be disabled when selectedTags.country is emmpty", async () => {
      //Arrange
      const wrapper = shallowMount(RequestInformation);
      const buttonComponent = createButtonComponent(wrapper);

      //Act
      wrapper.vm.selectedTags.country = [];
      await buttonComponent.vm.$nextTick();

      //Assert
      expect(buttonComponent.vm.disabled).toBeTruthy();
    });

    it("should be disabled when has been clicked and selectedTags were not changed", async () => {
      //Arrange
      const wrapper = shallowMount(RequestInformation);
      const buttonComponent = createButtonComponent(wrapper);

      //Act
      wrapper.vm.selectedTags.country = ["ANY_VALUE"];
      await wrapper.vm.$nextTick();
      buttonComponent.trigger("click");
      await buttonComponent.vm.$nextTick();

      //Assert
      expect(buttonComponent.vm.disabled).toBeTruthy();
    });

    it("should be enabled when has been clicked and selectedTags were changed", async () => {
      //Arrange
      const wrapper = shallowMount(RequestInformation);
      const buttonComponent = createButtonComponent(wrapper);

      //Act
      wrapper.vm.selectedTags.country = ["ANY_VALUE"];
      await wrapper.vm.$nextTick();
      buttonComponent.trigger("click");
      await buttonComponent.vm.$nextTick();
      expect(buttonComponent.vm.disabled).toBeTruthy();
      wrapper.vm.selectedTags.indicator = ["NEW_VALUE"];
      await wrapper.vm.$nextTick();

      //Assert
      expect(buttonComponent.vm.disabled).toBeFalsy();
    });
  });
});
