<script setup>
import SocialMediaLink from "./components/SocialMediaLink.vue";
import HeaderLogo from "./components/HeaderLogo.vue";
import ItensSelection from "./components/ItensSelection.vue";
</script>

<template>
  <header
    class="bg-headfoot container-fluid d-inline-flex justify-content-center shadow p-2 mb-4"
  >
    <HeaderLogo />
  </header>
  <main>
    <div class="bg-section p-1 mb-4">
      <section
        class="container text-center text-lg-start pe-0"
        aria-labelledby="section-text"
      >
        <h1 class="h1 fw-bold" id="section-text">What is this site about?</h1>
        <p>
          Do you want to know information about your country? This site will
          help you.
          <br />
          We provide information from the World Bank database and create graphs
          with this information.
          <br />
          <a href="https://databank.worldbank.org/" target="_blank">
            Read more about World Bank database
          </a>
        </p>
      </section>
    </div>
    <ItensSelection />
  </main>

  <footer
    class="bg-headfoot p-3 text-center container-fluid d-sm-inline-flex justify-content-center align-items-center"
  >
    <img
      src="./assets/logo.svg"
      alt="App logo"
      class="me-sm-5 img-sm-resize"
      width="110"
      height="110"
    />

    <span>
      <p class="text-sm-center fs-6">
        ©2022 by Yann Carvalho.
        <br />
        All Rights Reserved.
      </p>
      <SocialMediaLink />
    </span>
  </footer>
</template>
