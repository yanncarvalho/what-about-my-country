<script setup>
import { ref } from "vue";

const emit = defineEmits(["response"]);

const props = defineProps({
  content: {},
});

let elements = ref("");

function filter(event) {
  let text = event.target.value;
  //TODO tratar espaço em branco
  if (text === "") {
    elements.value = "";
  } else {
    elements.value = props.content.filter((co) =>
      co.text.toUpperCase().includes(text.toUpperCase())
    );
  }
}

function removeItem(event) {
  let element = event;
  elements.value = "";
  emit("response", element);
}
</script>

<template>
  <div>
    <label for="inputSearch" class="form-label m-0">Country</label>
    <input
      id="inputSearch"
      type="search"
      @input="filter"
      placeholder="Choose a country..."
      class="form-control bg-input--search rounded-3 p-2 me-1"
    />

    <div
      class="list-group position-absolute container rounded-3"
      id="list-tab"
      role="tablist"
    >
      <button
        v-for="element in elements"
        :key="element.id"
        class="list-group-item list-group-item-action bg-list--search"
        data-toggle="list"
        @click="removeItem(element)"
      >
        {{ element.text }}
      </button>
    </div>
  </div>
</template>

<style setup>
.bg-input--search {
  background-color: var(--color-primary-100) !important;
}
.bg-list--search {
  overflow: auto;
  z-index: 1000;
}
</style>