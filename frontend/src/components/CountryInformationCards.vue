<script setup>
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { computed, onUpdated, ref } from "vue";

const articleId = ref(null);

const props = defineProps({
  source: String,
  name: String,
  countryCodes: String,
});

let REQUEST = computed(() => {
  return gql`
  {
    country(codes: ${props.countryCodes}) {
      id
      name
      capitalCity
      latitude
      longitude
      region
      incomeLevel
    }
  }`;
});
let { result, loading, error } = useQuery(REQUEST);

function getFlagUrl(name) {
  let baseUrl = "../assets/flags/";
  let imageFormat = "svg";
  let fullUrl = baseUrl + name + "." + imageFormat;
  return new URL(fullUrl, import.meta.url).href;
}

function onErrorGetFlag(event) {
  let notFoundFlagUrl = "../assets/flag-not-found.png";
  event.target.src = new URL(notFoundFlagUrl, import.meta.url).href;
}

onUpdated(() => {
  if (articleId.value) {
    articleId.value.scrollIntoView({ behavior: "smooth" });
  }
});
</script>

<template>
  <div
    v-if="error || (result != null && result.lenght === 0)"
    class="alert alert-danger text-center"
    role="alert"
  >
    Something went wrong, it was not possible to load
    <b> Countries </b> information.
  </div>
  <div v-else-if="loading" class="alert alert-dark text-center" role="alert">
    Loading <b> Countries </b> information...
  </div>

  <article v-else class="container-fluid bg-section my-3 py-2" ref="articleId">
    <div class="container">
      <div
        class="row justify-content-start row-cols-1 row-cols-md-2 row-cols-lg-3 g-2"
      >
        <div class="col" v-for="country in result.country" :key="country.id">
          <div class="card h-100">
            <img
              class="card-img-top img-card"
              :alt="`Flag of ${country.name}`"
              :src="getFlagUrl(country.id.toLowerCase())"
              @error="(event) => onErrorGetFlag(event)"
            />

            <h5 class="card-header text-center fw-bold">{{ country.name }}</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <b>Capital city</b>: {{ country.capitalCity }}
              </li>
              <li class="list-group-item">
                <b>Region</b>: {{ country.region }}
              </li>
              <li class="list-group-item">
                <b>Income Level</b>: {{ country.incomeLevel }}
              </li>
              <li class="list-group-item">
                <b> Latitude</b>: {{ country.latitude }}
              </li>
              <li class="list-group-item">
                <b>Longitude</b>: {{ country.longitude }}
              </li>
            </ul>
            <div class="card-footer text-muted">
              <small>
                Source:&nbsp;
                <a
                  :href="source"
                  target="_blank"
                  :title="name"
                  aria-label="Link to see data source information"
                >
                  {{ name }}
                </a>
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>
