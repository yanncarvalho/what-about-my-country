import { describe, it, expect, beforeAll } from "vitest";
import { shallowMount } from "@vue/test-utils";
import RequestInformationDatalist from "src/components/RequestInformationDatalist.vue";

describe("Test Component RequestInformationDatalist", () => {
  let resultMock;
  let tagMock;
  beforeAll(() => {
    const baseValueMock = "Test";

    resultMock = {
      __type: {
        enumValues: [{ name: baseValueMock, description: baseValueMock }],
      },
    };
    tagMock = {
      key: baseValueMock,
      value: baseValueMock,
    };
  });
  /**
   * @description Mount RequestInformationDatalist Component and emit its event onResult
   * @returns {RequestInformationDatalist} RequestInformationDatalist Component
   */
  async function mountReqInfoDatalist() {
    let propsMock = {
      graphQLEnumName: "graphQLEnumName",
    };
    const wrapper = shallowMount(RequestInformationDatalist, {
      props: propsMock,
    });
    wrapper.vm.result = resultMock;
    await wrapper.trigger("onResult");
    return wrapper;
  }

  it("should add tagMock in onResult event", async () => {
    const wrapper = await mountReqInfoDatalist();
    const tagInput = wrapper.findComponent({ ref: "tagsInput" });
    await tagInput.vm.$emit("tagAdded", tagMock);
    const originalValue = tagMock;
    const emittedValue = wrapper.emitted().selectedElements[0][0]._value;
    expect(emittedValue).toStrictEqual([originalValue]);
  });

  it("should remove tagMock in onResult event", async () => {
    const wrapper = await mountReqInfoDatalist();
    const tagInput = wrapper.findComponent({ ref: "tagsInput" });
    await tagInput.vm.$emit("tagRemoved", tagMock);
    const emittedValue = wrapper.emitted().selectedElements[0][0]._value;
    expect(emittedValue).toHaveLength(0);
  });
});
