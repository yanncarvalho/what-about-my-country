<script setup>
import { watch, ref } from "vue";

const emit = defineEmits(["click"]);
const onClick = ref(null);

watch(onClick, () => {
  emit("click", onClick.value);
});

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
});
</script>

<template>
  <div class="d-flex container justify-content-center">
    <input
      type="submit"
      :value="value"
      :disabled="disabled"
      :title="value"
      :aria-label="ariaLabel"
      @click="(event) => (onClick = event)"
      class="btn btn-primary text-wrap px-sm-5 mb-2"
    />
  </div>
</template>
