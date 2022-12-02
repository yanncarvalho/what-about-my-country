<script setup>
import { ref } from "vue";
import LogoHeader from "./components/icons/LogoHeader.vue";
import RequestInformation from "./components/RequestInformation.vue";
import SocialMediaLink from "./components/SocialMediaLink.vue";
import ViewInformation from "./components/ViewInformation.vue";

const formResult = ref({
  country: Map,
  indicator: Map,
});
const sourceLink = {
  url: "https://databank.worldbank.org/",
  name: "World Bank",
};

function stringifyKeysObj(obj) {
  const regex = /"/g;
  for (const key of Object.keys(obj)) {
    let arr = obj[key];
    let keys = Array.isArray(arr) ? arr.map((o) => o.key) : arr;
    obj[key] = JSON.stringify(keys).replace(regex, "");
  }
  return obj;
}
</script>

<template>
  <header
    class="bg-headfoot container-fluid d-inline-flex justify-content-center shadow p-2 mb-4"
  >
    <LogoHeader />
  </header>
  <main>
    <div class="bg-primary p-1 mb-4">
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
          <a :href="sourceLink.url" target="_blank">
            Read more about World Bank database
          </a>
        </p>
      </section>
    </div>

    <RequestInformation @onResult="(r) => (formResult = r)" />
    <ViewInformation
      v-if="formResult.country !== null && formResult.country.length !== 0"
      :keys="stringifyKeysObj(formResult)"
      :sourceLink="sourceLink"
    />
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
