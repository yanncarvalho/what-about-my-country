<script setup>
import { ref } from "vue";
import RequestInformation from "./components/RequestInformation.vue";
import Footer from "./components/TheFooter.vue";
import Header from "./components/TheHeader.vue";
import ViewInformation from "./components/ViewInformation.vue";
import { scrollToId } from "./common/helpers.js";

const formResult = ref({
  country: Map,
  indicator: Map,
});
const reqInfoId = "requestInformation";
const urlSource = __APP_ENV__.REFERENCE_SOURCE_URL;
</script>

<template>
  <Header />
  <main>
    <div class="bg-primary p-1 mb-4">
      <section
        class="container text-center text-lg-start pe-0"
        aria-labelledby="section-text"
        id="section-main"
      >
        <h1 class="h1 fw-bold" id="section-main-text">
          What is this site about?
        </h1>
        <p>
          Do you want to know information about your country? This site will
          help you.
          <br />
          We provide information from the World Bank database and create graphs
          with this information.
          <br />
          <a :href="urlSource" target="_blank" id="section-main-link">
            Read more about World Bank database
          </a>
        </p>
      </section>
    </div>
    <RequestInformation @onResult="formResult = $event" :id="reqInfoId" />
    <ViewInformation
      ref="viewInformation"
      v-if="formResult.country !== null && formResult.country.length !== 0"
      :countries="formResult"
      @clickBtn="scrollToId(reqInfoId)"
    />
  </main>
  <Footer />
</template>
