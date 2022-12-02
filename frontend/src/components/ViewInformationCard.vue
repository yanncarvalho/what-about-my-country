<!-- eslint-disable no-unused-vars -->
<script setup>
const props = defineProps({
  sourceLink: {
    type: Object,
    required: true,
  },
  countryInfo: {
    type: Object,
    required: true,
  },
});

function getFlagUrl(name) {
  let baseUrl = "../assets/flags/";
  let imageFormat = "png";
  let fullUrl = baseUrl + name + "." + imageFormat;
  return new URL(fullUrl, import.meta.url).href;
}

function onErrorGetFlag(event) {
  let notFoundFlagUrl = "../assets/flag-not-found.png";
  event.target.src = new URL(notFoundFlagUrl, import.meta.url).href;
}
</script>

<template>
  <div class="card h-100">
    <img
      class="card-img-top card-img"
      :alt="`Flag of ${countryInfo.name}`"
      :src="getFlagUrl(countryInfo.id.toLowerCase())"
      @error="(event) => onErrorGetFlag(event)"
    />
    <h4
      class="card-header card-header-large text-center d-flex justify-content-center align-items-center fw-bold"
    >
      {{ countryInfo.name }}
    </h4>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">
        <b>Capital city</b>: {{ countryInfo.capitalCity }}
      </li>
      <li class="list-group-item"><b>Region</b>: {{ countryInfo.region }}</li>
      <li class="list-group-item">
        <b>Income Level</b>: {{ countryInfo.incomeLevel }}
      </li>
      <li class="list-group-item">
        <b>Latitude</b>: {{ countryInfo.latitude }}
      </li>
      <li class="list-group-item">
        <b>Longitude</b>: {{ countryInfo.longitude }}
      </li>
    </ul>
    <div class="card-footer text-muted">
      <small>
        Source:&nbsp;
        <a
          :href="sourceLink.url"
          target="_blank"
          :title="sourceLink.name"
          aria-label="Link to see data source information"
        >
          {{ sourceLink.name }}
        </a>
      </small>
    </div>
  </div>
</template>
