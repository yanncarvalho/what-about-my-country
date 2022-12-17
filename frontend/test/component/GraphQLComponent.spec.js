/* eslint-disable no-unused-labels */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { ref } from "vue";
import { mount, shallowMount } from "@vue/test-utils";
import GraphQLComponent from "src/components/GraphQLComponent.vue";

describe("Test Component GraphQLComponent", () => {
  let apollo;
  let propsMock;
  const errorMessage = "errorMessage";
  const loadingMessage = "loadingMessage";

  beforeEach(async () => {
    vi.mock("@vue/apollo-composable");
    propsMock = {
      query: "{}",
      errorMessage: errorMessage,
      loadingMessage: loadingMessage,
    };
    apollo = await import("@vue/apollo-composable");
  });
  describe("Test when error in receiving graphQL information", () => {
    beforeEach(() => {
      apollo.useQuery = () => {
        return {
          result: ref(undefined),
          loading: ref(undefined),
          error: ref([]),
        };
      };
    });

    it("should show div with ref error when error in processing query", () => {
      //Arrange
      const wrapper = mount(GraphQLComponent, { props: propsMock });
      const divError = wrapper.find({ ref: "error" });

      //Assert
      expect(divError.exists()).toBe(true);
    });

    it("should show error message when error in processing query", () => {
      //Arrange
      const wrapper = mount(GraphQLComponent, { props: propsMock });

      //Assert
      expect(wrapper.text()).toBe(errorMessage);
    });
  });
  describe("Test when loading graphQL information", () => {
    beforeEach(() => {
      apollo.useQuery = () => {
        return {
          result: ref(undefined),
          error: ref(undefined),
          loading: ref([]),
        };
      };
    });
    it("should show loading message when is processing query", () => {
      //Arrange
      const wrapper = mount(GraphQLComponent, { props: propsMock });
      const loadingDiv = wrapper.find({ ref: "loading" });

      //Assert
      expect(loadingDiv.exists()).toBe(true);
    });

    it("should show div with ref loading when is processing query", () => {
      //Arrange
      const wrapper = mount(GraphQLComponent, { props: propsMock });

      //Assert
      expect(wrapper.text()).toBe(loadingMessage);
    });
  });
  describe("Test when success in receiving  graphQL information", () => {
    const emitResult = "onResult";
    beforeEach(() => {
      apollo.useQuery = () => {
        return {
          result: ref([]),
          error: ref(undefined),
          loading: ref(undefined),
        };
      };
    });

    it("should emit result when its value change", async () => {
      //Arrange
      const wrapper = shallowMount(GraphQLComponent, { props: propsMock });

      //Act
      wrapper.vm.result = "anyValue";
      await wrapper.vm.$nextTick();

      //Assert
      expect(wrapper.emitted()).toHaveProperty(emitResult);
      expect(wrapper.emitted().onResult[0]).toStrictEqual([wrapper.vm.result]);
    });

    it("should not emit result when its value not change", () => {
      //Arrange
      const wrapper = shallowMount(GraphQLComponent, { props: propsMock });

      //Assert
      expect(wrapper.emitted()).not.toHaveProperty(emitResult);
    });
  });
});
