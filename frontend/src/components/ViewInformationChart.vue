<script setup>
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";
import "chart.js/auto";
import { computed } from "vue";
import { Line } from "vue-chartjs";
import ViewInformationSource from "./ViewInformationSource.vue";

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale);

const props = defineProps({
  labels: {
    required: true,
    type: Array,
  },
  datasets: {
    required: true,
    type: Array,
  },
  description: {
    required: true,
    type: String,
  },
  countriesNoData: {
    required: true,
    type: Array,
  },
});

const dataCollection = computed(() => {
  return {
    labels: props.labels,
    datasets: props.datasets,
  };
});
const chartHeight = 250;
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
          class="img-fluid p-2"
          src="@/assets/chart-not-found-data.png"
          alt="No data found from these countries"
        />
      </div>
      <Line
        v-else
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
          v-if="countriesNoData.length !== 0"
          class="fw-bold small text-danger"
        >
          No data from {{ countriesNoData.toString().replace(/,/g, ", ") }}.
          <br />
        </span>
        <ViewInformationSource />
      </div>
    </div>
  </div>
</template>
