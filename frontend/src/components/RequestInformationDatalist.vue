<script setup>
import TagsInput from "@voerro/vue-tagsinput";
import { ref, computed } from "vue";
import GraphQLComponent from "./GraphQLComponent.vue";
import { instropectEnumValue } from "../common/schemas.js";

const selectedTags = ref(new Array());
const result = ref(new Array());
const emit = defineEmits(["selectedElements"]);

emit("selectedElements", selectedTags);
const props = defineProps({
  label: {
    type: String,
    default: "Elements",
  },
  placeholder: {
    type: String,
    default: "Choose an element",
  },
  graphQLEnumName: {
    type: String,
    required: true,
  },
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

const query = computed(() => instropectEnumValue(props.graphQLEnumName));
</script>
<template>
  <div class="container mb-3" :aria-label="placeholder">
    <GraphQLComponent
      :loadingMensage="`Loading <b>${label}</b> options...`"
      :errorMensage="`Something went wrong, it was not possible to load <b> ${label} </b> options`"
      :query="query"
      @onResult="result = $event"
    />
    <div v-if="result && result.length !== 0">
      <label for="tagsInput" class="fw-bold">{{ label }}</label>
      <TagsInput
        ref="tagsInput"
        id="tagsInput"
        elementId="tags"
        @tagAdded="selectedTags.push($event)"
        @tagRemoved="
          (selectedTags = selectedTags.filter((v) => v.key !== $event.key))
        "
        :existingTags="
          result.__type.enumValues.map((type) => {
            return { key: type.name, value: type.description };
          })
        "
        :typeahead="true"
        :typeaheadHideDiscard="true"
        :typeaheadStyle="isDropDown ? 'dropdown' : 'badges'"
        :typeaheadMaxResults="maxResult"
        :typeaheadShowOnFocus="true"
        :onlyExistingTags="true"
        :addTagsOnSpace="true"
        :typeaheadAlwaysShow="alwaysShowOptions"
        :placeholder="
          result.__type.enumValues.length === selectedTags.length
            ? ''
            : placeholder
        "
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
