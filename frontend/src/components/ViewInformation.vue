<script setup>
import { computed, onUpdated, ref } from "vue";
import GraphQLComponent from "./GraphQLComponent.vue";
import ViewInformationCard from "./ViewInformationCard.vue";

const cardsRef = ref(null);
const result = ref([]);

const sourceLink = {
  url: "https://databank.worldbank.org/",
  name: "World Bank",
};
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
  <span ref="cardsRef">
    <GraphQLComponent
      :loadingMensage="`Loading information...`"
      :errorMensage="`Something went wrong, it was not possible to load information`"
      :query="query"
      @onResult="(r) => (result = r)"
    />

    <article
      class="container-fluid bg-primary my-3 py-2"
      v-if="result && result.length !== 0"
    >
      <div class="container">
        <div
          class="row justify-content-start row-cols-1 row-cols-md-2 row-cols-lg-3 g-2"
        >
          <div class="col" v-for="country in result.country" :key="country.id">
            <ViewInformationCard
              :countryInfo="country"
              :sourceLink="sourceLink"
            />
          </div>
        </div>
      </div>
    </article>
  </span>
</template>
