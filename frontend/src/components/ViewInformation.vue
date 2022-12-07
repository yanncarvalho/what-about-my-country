<script setup>
import { computed, onUpdated, ref, watch } from "vue";
import GraphQLComponent from "./GraphQLComponent.vue";
import ViewInformationCard from "./ViewInformationCard.vue";
import ViewInformationChart from "./ViewInformationChart.vue";
const cardsRef = ref(null);
const result = ref();
const indicators = ref();

watch(result, (res) => {
  indicators.value = {};
  res.country.forEach((country) => {
    country.indicators.forEach((indicator) => {
      if (!indicators.value[indicator.id]) {
        indicators.value[indicator.id] = {
          id: indicator["id"],
          description: indicator["description"],
          labels: new Set(),
          datasets: new Array(),
        };
      }

      let indiData = indicator.data.reduce(
        (a, v) => ({ ...a, [v.year]: v.value }),
        {}
      );
      Object.keys(indiData).forEach((key) => {
        indicators.value[indicator.id]["labels"].add(key);
      });

      indiData = [...indicators.value[indicator.id]["labels"]].map((v) => {
        return indiData[v] ?? NaN;
      });
      hasChart.value = indiData.length !== 0;
      indicators.value[indicator.id].datasets.push({
        data: indiData,
        label: country.name,
        borderColor: "#" + Math.floor(Math.random() * 16777215).toString(16),
        fill: false,
      });
    });
  });
});

const sourceLink = {
  url: "https://databank.worldbank.org/",
  name: "World Bank",
};

const hasChart = ref(false);

const props = defineProps({
  sourceLink: {
    type: Object,
    required: true,
  },
  keys: {
    type: Object,
    required: true,
  },
});
const query = computed(() => {
  return `
   {
    country(codes: ${props.keys.country}) {
      id,
      name,
      capitalCity,
      latitude,
      longitude,
      region,
      incomeLevel,
      indicators(ids:${props.keys.indicator}){
        id
        description,
        data{
              value,
              year
        }
      }
    }
   }`;
});
onUpdated(() => {
  if (cardsRef.value) {
    cardsRef.value.scrollIntoView({ behavior: "smooth" });
  }
});
</script>

<template>
  <article ref="cardsRef">
    <GraphQLComponent
      :loadingMensage="`Loading information...`"
      :errorMensage="`Something went wrong, it was not possible to load information`"
      :query="query"
      @onResult="(r) => (result = r)"
    />

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
              <ViewInformationCard
                :countryInfo="country"
                :sourceLink="sourceLink"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="my-4 bg-primary container-fluid" v-if="hasChart">
      <div class="container-lg pt-2">
        <h3 class="fw-bold">Charts</h3>
        <div v-for="indicator in indicators" :key="indicator.id">
          <ViewInformationChart
            v-if="indicator.datasets"
            :datasets="indicator.datasets"
            :labels="indicator.labels"
            :description="indicator.description"
            :sourceLink="sourceLink"
          />
        </div>
      </div>
    </section>
  </article>
</template>
