<script setup>
const referenceSrc = {
  url: __APP_ENV__.REFERENCE_SOURCE_URL,
  name: __APP_ENV__.REFERENCE_SOURCE_NAME,
};
</script>
<template>
  <small class="text-muted" id="reference-source">
    Source:&nbsp;
    <a
      id="reference-source-link"
      :href="referenceSrc.url"
      target="_blank"
      :title="referenceSrc.name"
      aria-label="Link to see data source information"
    >
      {{ referenceSrc.name }}
    </a>
  </small>
</template>
