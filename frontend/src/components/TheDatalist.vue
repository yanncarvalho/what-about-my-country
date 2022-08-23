<script setup>
import DatalistButton from "./DatalistButton.vue";
import { ref } from "vue";
let id = 0;
let iCountry = 0;
const elements = ref([
  { id: id++, text: "Brazil" },
  { id: id++, text: "Chile" },
  { id: id++, text: "Colombia" },
]);

const country = ref([
  { id: iCountry++, text: "Chile" },
  { id: iCountry++, text: "Colombia" },
]);

function removeElement(element) {
  elements.value = elements.value.filter((e) => e !== element);
}
</script>

<template>
  <div class="container pb-4">
    <div>
      <label for="countryDataList" class="form-label m-0">Country</label>
      <input
        class="form-select bg-datalist rounded-3 p-2 me-1"
        list="countryOptions"
        id="countryDataList"
        placeholder="Choose a country..."
      />

      <datalist id="countryOptions">
        <option v-for="coun in country" :key="coun.id">{{ coun.text }}</option>
      </datalist>
      <ul class="container d-flex flex-wrap justify-content-evenly text-center">
        <DatalistButton
          v-for="element in elements"
          :key="element.id"
          :text="element.text"
          @click="removeElement(element)"
        />
      </ul>
    </div>
  </div>
</template>

<style setup>
.bg-datalist {
  background-color: var(--color-primary-100) !important;
}
</style>