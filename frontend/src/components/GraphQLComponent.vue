<script setup>
import { useQuery } from "@vue/apollo-composable";
import { gql } from "graphql-tag";
import { computed, watch } from "vue";

const props = defineProps({
  idBase: {
    type: String,
    required: true,
  },
  query: {
    type: String,
    required: true,
  },
  loadingMessage: {
    type: String,
    default: "Loading...",
  },
  errorMessage: {
    type: String,
    default: "It was not possible to load",
  },
});
const { result, error, loading } = useQuery(
  computed(() => {
    return gql`
      ${props.query}
    `;
  })
);
const emit = defineEmits(["onResult"]);

watch(result, (res) => {
  emit("onResult", res);
});
</script>

<template>
  <div
    ref="error-div"
    :id="`error-${idBase}`"
    v-if="error"
    class="alert alert-danger text-center"
    role="alert"
    v-html="errorMessage"
  ></div>

  <div
    ref="loading-div"
    :id="`loading-${idBase}`"
    v-else-if="loading"
    class="alert alert-dark text-center"
    role="alert"
    v-html="loadingMessage"
  ></div>
</template>
