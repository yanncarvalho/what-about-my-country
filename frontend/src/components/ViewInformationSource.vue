<script setup>
import { referenceSource } from "../common/helpers.js";
</script>
<template>
  <small class="text-muted">
    Source:&nbsp;
    <a
      :href="referenceSource.url"
      target="_blank"
      :title="referenceSource.name"
      aria-label="Link to see data source information"
    >
      {{ referenceSource.name }}
    </a>
  </small>
</template>
