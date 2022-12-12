<script setup>
import { useQuery } from "@vue/apollo-composable";
import { gql } from "graphql-tag";
import { computed, watch } from "vue";

const props = defineProps({
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
    ref="error"
    v-if="error"
    class="alert alert-danger text-center"
    role="alert"
    v-html="errorMessage"
  ></div>

  <div
    ref="loading"
    v-else-if="loading"
    class="alert alert-dark text-center"
    role="alert"
    v-html="loadingMessage"
  ></div>
</template>
