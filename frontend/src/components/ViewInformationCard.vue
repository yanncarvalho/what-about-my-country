<!-- eslint-disable no-unused-vars -->
<script setup>
import ViewInformationSource from "./ViewInformationSource.vue";
import { inject } from "vue";

const { FLAG } = inject("application_config");

const props = defineProps({
  countryInfo: {
    type: Object,
    required: true,
  },
});

/**
 * @description create flag image url
 * @param {string} flagCode country code of the flag
 * @returns {URL} flag image url
 */
function getFlagUrl(flagCode) {
  const { BASE_URL, IMAGE_FORMAT } = FLAG.REQUEST;
  const path = `${BASE_URL}/${flagCode}.${IMAGE_FORMAT}`;
  return new URL(path, import.meta.url);
}

/**
 * @description set event src with flag_not_found url
 * @param {Event} event error Event
 */
function onErrorGetFlagNotFound(event) {
  event.target.src = new URL(FLAG.NOT_FOUND, import.meta.url);
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
