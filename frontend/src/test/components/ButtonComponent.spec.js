import { describe, it, expect, beforeAll } from "vitest";
import { mount } from "@vue/test-utils";
import ButtonComponent from "src/components/ButtonComponent.vue";

describe("Test Component ButtonComponent", () => {
  let propsMock;
  beforeAll(() => {
    propsMock = {
      ariaLabel: "ariaLabel",
      value: "value",
    };
  });
  it("should be target click event when button is clicked", () => {
    const wrapper = mount(ButtonComponent, { props: propsMock });
    wrapper.find({ ref: "BtnButtonComponent" }).trigger("click");
    expect(wrapper.emitted()).toHaveProperty("click");
  });
});
