<script setup>
import { getLogoUrl } from "@/common/helpers";
import LogoHeaderText from "./LogoHeaderText.vue";
</script>

<template>
  <h1 class="justify-content-center text-center" role="presentation">
    <img
      :src="getLogoUrl()"
      alt="App logo"
      class="logo-img-880-resize me-1"
      width="110"
      height="110"
    />
    <LogoHeaderText />
  </h1>
</template>
