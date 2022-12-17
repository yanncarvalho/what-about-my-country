<script setup>
// eslint-disable-next-line no-unused-vars
const props = defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
  value: {
    type: String,
    required: true,
  },
  ariaLabel: {
    type: String,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
  typeBtn: {
    type: String,
    default: "button",
  },
});
</script>

<template>
  <input
    :ref="id"
    :id="id"
    :type="typeBtn === 'submit' ? 'submit' : 'button'"
    :value="value"
    :disabled="disabled"
    :title="value"
    :aria-label="ariaLabel"
    class="btn btn-primary text-wrap px-sm-5 mb-2"
  />
</template>
