<script setup>
import AutocompleteSearch from "./AutocompleteSearch.vue";
import { ref } from "vue";

let id = 0;
const btnElements = ref([]);
const searchElements = ref([
  { id: id++, text: "Chile" },
  { id: id++, text: "Brazil" },
  { id: id++, text: "Angola" },
  { id: id++, text: "repulic C" },
  { id: id++, text: "B d" },
  { id: id++, text: "Bil" },
]);

function bindBtnSearchElem(element) {
  const isElementInSearch = searchElements.value.some(
    (x) => x.id === element.id
  );

  if (isElementInSearch) {
    btnElements.value.push(element);
    searchElements.value = searchElements.value.filter(
      (x) => x.id != element.id
    );
  } else {
    searchElements.value.push(element);
    btnElements.value = btnElements.value.filter((x) => x.id != element.id);
  }
}
</script>

<template>
  <div class="container pb-4">
    <div>
      <AutocompleteSearch
        :content="searchElements"
        @response="(resp) => bindBtnSearchElem(resp)"
      />
      <ul
        class="container d-flex flex-wrap justify-content-evenly text-center"
        role="toolbar"
      >
        <li
          class="list-group-item"
          v-for="btn in btnElements"
          :key="btn.id"
          @click="bindBtnSearchElem(btn)"
        >
          <button
            class="btn bg-btn__itens m-1 p-2 pe-lg-5 ps-lg-5 rounded-4"
            :text="btn.text"
          >
            {{ btn.text }}
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<style setup>
.bg-btn__itens:hover {
  background-color: var(--color-primary-100) !important;
}
.bg-btn__itens {
  background-color: var(--color-primary-70) !important;
}
</style>