<script setup>
import LogoHeaderText from "./LogoHeaderText.vue";
import { inject } from "vue";

const { LOGO } = inject("application_config");
</script>

<template>
  <h1 class="justify-content-center text-center" role="presentation">
    <img
      :src="LOGO.PATH"
      alt="App logo"
      class="logo-img-880-resize me-1"
      width="110"
      height="110"
    />
    <LogoHeaderText />
  </h1>
</template>
