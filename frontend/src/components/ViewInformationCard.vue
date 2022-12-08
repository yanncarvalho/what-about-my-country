<!-- eslint-disable no-unused-vars -->
<script setup>
import ViewInformationSource from "./ViewInformationSource.vue";
import { getFlagUrl, getFlagNotFound } from "../common/helpers";

const props = defineProps({
  countryInfo: {
    type: Object,
    required: true,
  },
});

function onErrorGetFlagNotFound(event) {
  event.target.src = getFlagNotFound().href;
}
</script>

<template>
  <div class="card h-100">
    <img
      class="card-img-top card-img"
      :alt="`Flag of ${countryInfo.name}`"
      :src="getFlagUrl(countryInfo.id.toLowerCase()).href"
      @error="onErrorGetFlagNotFound($event)"
    />
    <h4
      class="card-header card-header-large text-center d-flex justify-content-center align-items-center fw-bold bg-secondary"
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
    <div class="card-footer text-muted bg-secondary">
      <ViewInformationSource />
    </div>
  </div>
</template>
