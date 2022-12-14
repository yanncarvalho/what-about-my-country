<script setup>
import { inject } from "vue";
const { REFERENCE_SOURCE } = inject("application_config");
</script>
<template>
  <small class="text-muted">
    Source:&nbsp;
    <a
      :href="REFERENCE_SOURCE.URL"
      target="_blank"
      :title="REFERENCE_SOURCE.NAME"
      aria-label="Link to see data source information"
    >
      {{ REFERENCE_SOURCE.NAME }}
    </a>
  </small>
</template>
