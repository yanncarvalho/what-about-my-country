<script setup>
import { computed, onUpdated, ref, watch } from "vue";
import {
  genChartsIndicator,
  stringifyKeyObj,
  scrollToId,
} from "@/common/helpers.js";
import { selectCountries } from "@/common/schemas.js";
import GraphQLComponent from "./GraphQLComponent.vue";
import ViewInformationCard from "./ViewInformationCard.vue";
import ViewInformationChart from "./ViewInformationChart.vue";
import Button from "./ButtonComponent.vue";

const result = ref();
const indicators = ref();

const props = defineProps({
  countries: {
    type: Object,
    required: true,
  },
});
const query = computed(() => {
  const code = stringifyKeyObj(props.countries.country);
  const ids = stringifyKeyObj(props.countries.indicator);
  return selectCountries(code, ids);
});
const cardId = "cardId";

watch(result, (res) => {
  const indicator = props.countries.indicator;
  const countries = res.country;
  indicators.value = genChartsIndicator(indicator, countries);
});

onUpdated(() => {
  scrollToId(cardId);
});
</script>

<template>
  <article :id="cardId">
    <GraphQLComponent
      :loadingMensage="`Loading information...`"
      :errorMensage="`Something went wrong, it was not possible to load information`"
      :query="query"
      @onResult="result = $event"
    />
    <div v-if="result && result.length !== 0">
      <section
        class="container-fluid bg-primary my-3 py-2"
        v-if="result && result.length !== 0"
      >
        <div class="container">
          <h3 class="fw-bold">Countries</h3>
          <div
            class="row justify-content-start row-cols-1 row-cols-md-2 row-cols-lg-3 g-2"
          >
            <div v-for="country in result.country" :key="country.id">
              <div class="col">
                <ViewInformationCard :countryInfo="country" />
              </div>
            </div>
          </div>
        </div>
      </section>
      <section
        class="my-4 bg-primary container-fluid"
        v-if="indicators && Object.keys(indicators).length !== 0"
      >
        <div class="container-lg pt-2">
          <h3 class="fw-bold">Charts</h3>
          <div v-for="indicator in indicators" :key="indicator.id">
            <ViewInformationChart
              :datasets="indicator.datasets"
              :labels="indicator.labels"
              :description="indicator.description"
              :countriesWithoutData="
                result.country
                  .filter(({ id }) => !indicator.countryIds.has(id))
                  .map(({ name }) => name)
              "
            />
          </div>
        </div>
      </section>
      <Button
        @click="$emit('clickBtn', $event)"
        value="Go back to choose more countries!"
        ariaLabel="Click to roll back to choose more countris"
      />
    </div>
  </article>
</template>
