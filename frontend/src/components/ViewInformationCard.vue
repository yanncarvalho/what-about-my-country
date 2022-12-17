<script setup>
import ViewInformationSource from "./ViewInformationSource.vue";

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  countryInfo: {
    type: Object,
    required: true,
  },
});

/**
 * @description get image flag url
 * @param {string} flagCode country code for the flag
 * @returns {URL} image flag url
 */
function getFlagUrl(flagCode) {
  const baseUrl = __APP_ENV__.FLAG_REQUEST_BASE_URL;
  const imageFormat = __APP_ENV__.FLAG_REQUEST_IMAGE_FORMAT;

  const path = `${baseUrl}/${flagCode}.${imageFormat}`;
  return new URL(path, import.meta.url);
}

/**
 * @description set event src with flag_not_found url
 * @param {Event} event error event
 */
function getErrorGetFlagNotFound(event) {
  const flagNotFound = __APP_ENV__.FLAG_NOT_FOUND_PATH;
  event.target.src = new URL(flagNotFound, import.meta.url);
}
</script>

<template>
  <div class="card h-100">
    <img
      ref="cardImg"
      class="card-img-top card-img"
      :alt="`Flag of ${countryInfo.name}`"
      :src="getFlagUrl(countryInfo.id.toLowerCase())"
      @error="getErrorGetFlagNotFound($event)"
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
