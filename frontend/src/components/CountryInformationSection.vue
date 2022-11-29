<script setup>
const props = defineProps({
  countryName: String,
});
console.log(props.countryName);
</script>

<template>
  <div class="container p-1 mb-4 d-row-flex justify-content-center bg-section">
    <section aria-labelledby="section-text">
      <h4>{{ countryName }}</h4>
      <p class="text-center text-lg-start p-2 bg-section">TEXTO B</p>
    </section>
  </div>
</template>
