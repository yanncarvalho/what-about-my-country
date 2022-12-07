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

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale);

const props = defineProps({
  labels: Set,
  datasets: Array,
  description: String,
  sourceLink: {
    type: Object,
    required: true,
  },
});

const datacollection = computed(() => {
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
      <Line
        :chartData="datacollection"
        :height="chartHeight"
        class="pb-2 pt-0 px-2"
      />
    </div>
    <div
      class="bg-secondary h-100 m-0 p-2 rounded-bottom w-100 border border-top-0"
    >
      <small class="text-muted">
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
