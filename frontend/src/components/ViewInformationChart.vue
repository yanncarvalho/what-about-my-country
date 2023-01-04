<script setup>
import chartNotFoundImage from "@/assets/images/chart-not-found-data.png";
import {
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";
import "chart.js/auto";
import { computed } from "vue";
import { Line } from "vue-chartjs";
import ViewInformationSource from "./ViewInformationSource.vue";

const props = defineProps({
  labels: {
    type: Array,
    required: true,
  },
  idBase: {
    type: String,
    required: true,
  },
  datasets: {
    type: Array,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  countriesWithoutData: {
    type: Array,
    required: true,
  },
  chartHeight: {
    type: Number,
    default: 250,
  },
});

const dataCollection = computed(
  () =>
    new Object({
      labels: props.labels,
      datasets: props.datasets,
    })
);

Chart.register(Title, Tooltip, Legend, CategoryScale, LinearScale);
</script>
<template>
  <div class="pb-4">
    <h4
      :id="`chart-label-${idBase}`"
      class="fw-bold text-center bg-secondary h-100 m-0 py-3 rounded-top border"
    >
      {{ description }}
    </h4>
    <div class="bg-white m-0 border border-top-0">
      <div
        v-if="dataCollection.datasets.length === 0"
        class="d-flex justify-content-center"
      >
        <img
          :id="`chart-notfound-${idBase}`"
          ref="notFoundImg"
          class="img-fluid p-2"
          :src="chartNotFoundImage"
          alt="No data found from these countries"
        />
      </div>
      <Line
        v-else
        ref="chart"
        :id="`chart-view-${idBase}`"
        :data="dataCollection"
        :height="chartHeight"
        class="pb-2 pt-0 px-2"
        data-cy="chart-view"
      />
    </div>
    <div
      class="bg-secondary h-100 m-0 p-2 rounded-bottom w-100 border border-top-0"
    >
      <div
        v-if="dataCollection.datasets.length !== 0"
        :id="`chart-footer-countries-${idBase}`"
      >
        <span
          v-if="countriesWithoutData.length !== 0"
          class="fw-bold small text-danger"
          :id="`chart-notfound-countries-${idBase}`"
        >
          No data from
          {{ countriesWithoutData.toString().replace(/,/g, ", ") }}.
          <br />
        </span>
        <ViewInformationSource />
      </div>
    </div>
  </div>
</template>
