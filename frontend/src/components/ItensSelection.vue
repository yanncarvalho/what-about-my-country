<script setup>
import TagsInput from "@voerro/vue-tagsinput/src/VoerroTagsInput.vue";

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  label: String,
  placeholder: String,
});
</script>

<template>
  <div class="container mb-3" :aria-label="placeholder">
    <label for="tagsInput" class="fw-bold">{{ label }}</label>
    <TagsInput
      id="tagsInput"
      element-id="tags"
      v-model="selectedTags"
      :existing-tags="[
        { key: 'web-development', value: 'Web Development' },
        { key: 'php', value: 'PHP' },
        { key: 'javascript', value: 'JavaScript' },
      ]"
      :typeahead="true"
      typeahead-max-results="8"
      typeahead-hide-discard="true"
      only-existing-tags="true"
      typeahead-style="dropdown"
      add-tags-on-space="true"
      :placeholder="placeholder"
    >
    </TagsInput>
  </div>
</template>

<style setup>
@import url("@voerro/vue-tagsinput/dist/style.css");
.tags-input-typeahead-item-default {
  color: var(--color-text);
  background-color: var(--color-primary-70);
}

.tags-input-typeahead-item-highlighted-default {
  color: var(--color-text);
  background-color: var(--color-grey-40) !important;
}

.tags-input-badge-selected-default {
  color: var(--color-text);
  background-color: var(--color-grey-20);
}

/* Typeahead */
.typeahead-hide-btn {
  color: var(--color-primary-70) !important;
}

.tags-input-remove:before,
.tags-input-remove:after {
  background-color: red;
}
.tags-input-wrapper-default {
  background-color: var(--color-primary-40);
  border-color: none;
}
</style>
