<script setup>
import SocialMediaLink from "./SocialMediaLink.vue";
import { inject } from "vue";

const { LOGO } = inject("application_config");
</script>
<template>
  <footer
    class="bg-headfoot p-5 mt-5 mb-0 text-center container-fluid d-sm-inline-flex justify-content-center align-items-center"
  >
    <img
      :src="LOGO.PATH"
      alt="App logo"
      class="me-sm-5 logo-img-sm-resize pb-sm-20px pt-1"
      width="200"
      height="200"
    />

    <span>
      <p class="text-sm-center fs-4">
        ©2022 by Yann Carvalho.
        <br />
        All Rights Reserved.
      </p>
      <SocialMediaLink />
    </span>
  </footer>
</template>
