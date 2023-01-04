<script setup>
import SocialMediaLink from "./SocialMediaLink.vue";
</script>
<template>
  <footer
    class="bg-headfoot p-5 mt-5 mb-0 text-center container-fluid d-sm-inline-flex justify-content-center align-items-center"
  >
    <img
      id="logo-footer"
      src="@/assets/images/logo.svg"
      alt="App logo"
      class="me-sm-5 logo-img-sm-resize pb-sm-20px pt-1"
      width="200"
      height="200"
    />

    <span>
      <p class="text-sm-center fs-4" id="copyright-footer">
        ©2023 by Yann Carvalho.
        <br />
        All Rights Reserved.
      </p>
      <SocialMediaLink />
    </span>
  </footer>
</template>
