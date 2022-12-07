<script setup>
import { computed, onUpdated, ref, watch } from "vue";
import GraphQLComponent from "./GraphQLComponent.vue";
import ViewInformationCard from "./ViewInformationCard.vue";
import ViewInformationChart from "./ViewInformationChart.vue";
const cardsRef = ref(null);
const result = ref();
const indicators = ref();

watch(result, (res) => {
  indicators.value = props.countries.indicator.reduce(
    (o, item) => ({
      ...o,
      [item.key]: new Object({
        id: item.key,
        description: item.value,
        labels: new Array(),
        datasets: new Array(),
        countryIds: new Set(),
      }),
    }),
    {}
  );

  res.country.forEach((country) => {
    country.indicators.forEach((indicator) => {
      indicators.value[indicator.id].countryIds.add(country.id);
      let indiData = indicator.data
        .slice()
        .reduce((a, v) => ({ ...a, [v.year]: v.value }), {});
      let countryIndi = indicators.value[indicator.id];
      Object.keys(indiData).forEach((key) => {
        if (!countryIndi.labels.includes(key)) {
          countryIndi.labels.push(key);
        }
      });
      indicators.value[indicator.id].labels = countryIndi.labels.sort(
        (a, b) => a - b
      );

      indiData = indicators.value[indicator.id].labels.map((v) => {
        return indiData[v] ?? NaN;
      });
      indicators.value[indicator.id].datasets.push({
        data: indiData,
        label: country.name,
        borderColor: generateRandomColor(),
        fill: false,
      });
    });
  });
});

function generateRandomColor() {
  return "#" + Math.floor(Math.random() * 16777215).toString(16);
}

function stringifyKeyObj(obj) {
  const regex = /"/g;
  let keys = Object.values(obj).map((o) => o.key) ?? [];
  return JSON.stringify(keys).replace(regex, "");
}

const props = defineProps({
  countries: {
    type: Object,
    required: true,
  },
});

const query = computed(() => {
  return `
   {
    country(codes:  ${stringifyKeyObj(props.countries.country)} ) {
      id,
      name,
      capitalCity,
      latitude,
      longitude,
      region,
      incomeLevel,
      indicators(ids: ${stringifyKeyObj(props.countries.indicator)}) {
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
              <ViewInformationCard :countryInfo="country" />
            </div>
          </div>
        </div>
      </div>
    </section>
    <section
      class="my-4 bg-primary container-fluid"
      v-show="!indicators || Object.keys(indicators).length !== 0"
    >
      <div class="container-lg pt-2">
        <h3 class="fw-bold">Charts</h3>
        <div v-for="indicator in indicators" :key="indicator.id">
          <ViewInformationChart
            :datasets="indicator.datasets"
            :labels="indicator.labels"
            :description="indicator.description"
            :countriesNoData="
              result.country
                .filter((c) => !indicator.countryIds.has(c.id))
                .map((c) => c.name)
            "
          />
        </div>
      </div>
    </section>
  </article>
</template>
