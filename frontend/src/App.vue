<script setup>
import { ref } from "vue";
import CountryInformationCards from "./components/CountryInformationCards.vue";
import GraphQLEnumDatalist from "./components/GraphQLEnumDatalist.vue";
import HeaderLogo from "./components/HeaderLogo.vue";
import SocialMediaLink from "./components/SocialMediaLink.vue";

const selectedTags = ref({
  country: [],
  indicator: [],
});

let buttonSelection = ref({
  country: [],
  indicator: [],
});

const informationSource = {
  link: "https://databank.worldbank.org/",
  text: "World Bank",
};

function onClickShowCountries() {
  buttonSelection.value = JSON.parse(JSON.stringify(selectedTags.value));
  let countryCards = document.getElementById("countryCards");
  if (countryCards) {
    countryCards.scrollIntoView({ behavior: "smooth" });
  }
}

function convertKeysToString(keys) {
  return JSON.stringify(keys).replace(/"/g, "");
}
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
          <a :href="informationSource.link" target="_blank">
            Read more about World Bank database
          </a>
        </p>
      </section>
    </div>
    <GraphQLEnumDatalist
      @selectedTags="(v) => (selectedTags.country = v)"
      label="Country"
      placeholder="Choose a Country"
      graphQLEnumName="Code"
      :isDropDown="true"
      :maxResult="6"
    />
    <GraphQLEnumDatalist
      @selectedTags="(v) => (selectedTags.indicator = v)"
      label="Indicator"
      placeholder="Choose an Indicator"
      graphQLEnumName="IndicatorId"
      :alwaysShowOptions="true"
    />
    <div class="d-flex container justify-content-center">
      <a
        role="button"
        disabled
        :class="{
          disabled:
            selectedTags.country.length === 0 ||
            Object.entries(buttonSelection).toString() ===
              Object.entries(selectedTags).toString(),
        }"
        title="Show me these countries"
        class="btn btn-primary text-wrap px-sm-5 mb-2"
        aria-label="Click to show information about selected countries"
        @click="onClickShowCountries"
      >
        Show me these countries
      </a>
    </div>
    <CountryInformationCards
      id="countryCards"
      v-if="
        buttonSelection.country !== null && buttonSelection.country.length !== 0
      "
      :countryCodes="
        convertKeysToString(buttonSelection.country.map((c) => c.key))
      "
      :source="informationSource.link"
      :name="informationSource.text"
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
