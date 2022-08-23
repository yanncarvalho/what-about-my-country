<script setup>
const props = defineProps({
  text: String,
});
</script>

<template>
  <button
    type="button"
    class="btn bg-chosen cursor-chosen m-1 p-2 pe-lg-5 ps-lg-5 rounded-4"
  >
    {{ text }}
  </button>
</template>

<style setup>
.bg-chosen:hover {
  background-color: var(--color-primary-100) !important;
}
.bg-chosen {
  background-color: var(--color-primary-70) !important;
}
</style>