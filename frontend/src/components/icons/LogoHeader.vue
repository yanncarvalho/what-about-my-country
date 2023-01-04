<script setup>
import LogoHeaderText from "./LogoHeaderText.vue";
</script>

<template>
  <h1
    class="justify-content-center text-center"
    role="presentation"
    id="logo-header"
  >
    <img
      id="logo-image"
      src="@/assets/images/logo.svg"
      alt="App logo"
      class="logo-img-880-resize me-1"
      width="110"
      height="110"
    />
    <LogoHeaderText />
  </h1>
</template>
