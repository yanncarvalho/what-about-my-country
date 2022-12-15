<script setup>
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
import { inject } from "vue";

const { CHART } = inject("application_config");

const props = defineProps({
  labels: {
    type: Array,
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
          ref="notFoundImg"
          class="img-fluid p-2"
          :src="CHART.NOT_FOUND_PATH"
          alt="No data found from these countries"
        />
      </div>
      <Line
        v-else
        ref="chart"
        :chartData="dataCollection"
        :height="chartHeight"
        class="pb-2 pt-0 px-2"
      />
    </div>
    <div
      class="bg-secondary h-100 m-0 p-2 rounded-bottom w-100 border border-top-0"
    >
      <div v-if="dataCollection.datasets.length !== 0">
        <span
          v-if="countriesWithoutData.length !== 0"
          class="fw-bold small text-danger"
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
