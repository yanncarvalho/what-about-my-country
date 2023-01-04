<script setup>
import {
  genChartsIndicator,
  scrollToId,
  stringifyKeyObj,
} from "@/common/helpers.js";
import { selectCountries } from "@/common/schemas.js";
import { computed, onUpdated, ref, watch } from "vue";
import Button from "./ButtonComponent.vue";
import GraphQLComponent from "./GraphQLComponent.vue";
import ViewInformationCard from "./ViewInformationCard.vue";
import ViewInformationChart from "./ViewInformationChart.vue";

const result = ref();
const chartData = ref();

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

const emit = defineEmits(["clickBtn"]);

function clickBtn(event) {
  emit("clickBtn", event);
}
watch(result, (res) => {
  const indicator = props.countries.indicator;
  const countries = res.country;
  chartData.value = genChartsIndicator(indicator, countries);
});

onUpdated(() => {
  scrollToId(cardId);
});
</script>

<template>
  <article :id="cardId">
    <GraphQLComponent
      :idBase="`country-code-graphql`"
      :loadingMensage="`Loading information...`"
      :errorMensage="`Something went wrong, it was not possible to load information`"
      :query="query"
      @onResult="result = $event"
    />

    <div v-if="result && result.length !== 0" id="countries">
      <section
        class="container-fluid bg-primary my-3 py-2"
        id="viewinformation-section"
      >
        <div class="container">
          <h3 class="fw-bold" id="viewinformation-country-label">Countries</h3>
          <div
            class="row justify-content-start row-cols-1 row-cols-md-2 row-cols-lg-3 g-2"
            data-cy="country-cards"
          >
            <div v-for="country in result.country" :key="country.id">
              <div class="col">
                <ViewInformationCard
                  :idBase="country.id"
                  ref="viewInformationCard"
                  :countryInfo="country"
                />
              </div>
            </div>
          </div>
        </div>
      </section>
      <section
        class="my-4 bg-primary container-fluid"
        v-if="chartData && Object.keys(chartData).length !== 0"
      >
        <div class="container-lg pt-2" id="charts">
          <h3 class="fw-bold">Charts</h3>

          <div v-for="datum in chartData" :key="datum.id">
            <ViewInformationChart
              ref="viewInformationChart"
              :idBase="datum.id"
              :datasets="datum.datasets"
              :labels="datum.labels"
              :description="datum.description"
              :countriesWithoutData="
                result.country
                  .filter(({ id }) => !datum.countryIds.has(id))
                  .map(({ name }) => name)
              "
            />
          </div>
        </div>
      </section>
      <div class="d-flex container justify-content-center">
        <Button
          data-cy="goBackButton"
          id="goBackButton"
          @click="clickBtn($event)"
          value="Go back to choose more countries!"
          ariaLabel="Click to roll back to choose more countries"
        />
      </div>
    </div>
  </article>
</template>
