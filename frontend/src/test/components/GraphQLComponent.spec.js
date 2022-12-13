/* eslint-disable no-unused-labels */
import { describe, it, expect, vi, beforeAll, afterEach } from "vitest";
import { ref } from "vue";
import { mount, shallowMount } from "@vue/test-utils";
import GraphQLComponent from "src/components/GraphQLComponent.vue";

describe("Test Component GraphQLComponent", () => {
  let apollo;
  let propsMock;
  const errorMessage = "errorMessage";
  const loadingMessage = "loadingMessage";

  beforeAll(async () => {
    vi.mock("@vue/apollo-composable");
    propsMock = {
      query: "{}",
      errorMessage: errorMessage,
      loadingMessage: loadingMessage,
    };
    apollo = await import("@vue/apollo-composable");
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("When error in receiving graphQL information", () => {
    beforeAll(() => {
      apollo.useQuery = () => {
        return {
          result: ref(undefined),
          loading: ref(undefined),
          error: ref(new Object()),
        };
      };
    });

    it("should show div with ref error when error in processing query", async () => {
      const wrapper = mount(GraphQLComponent, { props: propsMock });
      const divError = wrapper.find({ ref: "error" });
      expect(divError.exists()).toBe(true);
    });

    it("should show error message when error in processing query", async () => {
      const wrapper = mount(GraphQLComponent, { props: propsMock });
      expect(wrapper.text()).toBe(errorMessage);
    });
  });
  describe("When loading graphQL information", () => {
    beforeAll(() => {
      apollo.useQuery = () => {
        return {
          result: ref(undefined),
          error: ref(undefined),
          loading: ref(new Object()),
        };
      };
    });
    it("should show loading message when is processing query", async () => {
      const wrapper = mount(GraphQLComponent, { props: propsMock });
      const loadingDiv = wrapper.find({ ref: "loading" });
      expect(loadingDiv.exists()).toBe(true);
    });

    it("should show div with ref loading when is processing query", async () => {
      const wrapper = mount(GraphQLComponent, { props: propsMock });
      expect(wrapper.text()).toBe(loadingMessage);
    });
  });
  describe("When success in receiving  graphQL information", () => {
    const emitResult = "onResult";
    beforeAll(() => {
      apollo.useQuery = () => {
        return {
          result: ref([]),
          error: ref(undefined),
          loading: ref(undefined),
        };
      };
    });

    it("should emit result when its value change", async () => {
      const wrapper = shallowMount(GraphQLComponent, { props: propsMock });
      wrapper.vm.result = "anyValue";
      await wrapper.vm.$nextTick();
      expect(wrapper.emitted()).toHaveProperty(emitResult);
      expect(wrapper.emitted().onResult[0]).toStrictEqual([wrapper.vm.result]);
    });

    it("should not emit result when its value not change", async () => {
      const wrapper = shallowMount(GraphQLComponent, { props: propsMock });
      expect(wrapper.emitted()).not.toHaveProperty(emitResult);
    });
  });
});
