<script setup>
import TagsInput from "@voerro/vue-tagsinput/src/VoerroTagsInput.vue";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
const props = defineProps({
  label: String,
  placeholder: String,
  graphQLEnumName: String,

  alwaysShowOptions: {
    type: Boolean,
    default: false,
  },

  isDropDown: {
    type: Boolean,
    default: false,
  },

  maxResult: {
    type: Number,
    default: 0,
  },
});

const REQUEST = gql`
  {
    __type(name: "${props.graphQLEnumName}") {
      enumValues {
        name
        description
      }
    }
  }
`;

const { result, loading, error } = useQuery(REQUEST);
</script>
//v-for="type in result" :key="type.name"> // {{ type.description }}
<template>
  <div class="container mb-3" :aria-label="placeholder">
    <div
      v-if="error || (result != null && result.__type === null)"
      class="alert alert-danger text-center"
      role="alert"
    >
      Something went wrong, it was not possible to loading
      <strong>{{ label }}</strong> options
    </div>
    <div
      v-else-if="loading || result.enumValues"
      class="alert alert-dark text-center"
      role="alert"
    >
      Loading <strong>{{ label }}</strong> options...
    </div>
    <div v-else>
      <label for="tagsInput" class="fw-bold">{{ label }}</label>
      <TagsInput
        id="tagsInput"
        element-id="tags"
        v-model="selectedTags"
        :existing-tags="
          result.__type.enumValues.map((type) => {
            return { key: type.name, value: type.description };
          })
        "
        :typeahead="true"
        :typeahead-hide-discard="true"
        :typeahead-style="isDropDown ? 'dropdown' : 'badges'"
        :typeahead-max-results="maxResult"
        :typeahead-show-on-focus="true"
        :only-existing-tags="true"
        :add-tags-on-space="true"
        :typeahead-always-show="alwaysShowOptions"
        :placeholder="placeholder"
      >
      </TagsInput>
    </div>
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
