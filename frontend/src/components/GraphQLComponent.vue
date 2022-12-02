<script setup>
import { useQuery } from "@vue/apollo-composable";
import { gql } from "graphql-tag";
import { computed, watch } from "vue";

const props = defineProps({
  query: {
    type: String,
    required: true,
  },
  loadingMensage: {
    type: String,
    default: "Loading...",
  },
  errorMensage: {
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

watch(result, () => {
  emit("onResult", result.value);
});
</script>

<template>
  <div
    v-if="error"
    class="alert alert-danger text-center"
    role="alert"
    v-html="errorMensage"
  ></div>

  <div
    v-else-if="loading"
    class="alert alert-dark text-center"
    role="alert"
    v-html="loadingMensage"
  ></div>
</template>
