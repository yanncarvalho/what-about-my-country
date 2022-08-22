<script setup></script>

<template>
  <div>
    <div class="container pb-4">
      <label for="countryDataList" class="form-label m-0">Country</label>
      <input
        class="form-select bg-datalist rounded-3 p-2 text-center"
        list="countryOptions"
        id="countryDataList"
        placeholder="Choose a country..."
      />

      <datalist id="countryOptions">
        <option value="Brazil"></option>
        <option value="Chile"></option>
        <option value="Colombia"></option>
      </datalist>
    </div>
    <div
      class="container d-flex flex-row mb-3 justify-content-evenly text-center"
    >
      <div class="bg-chosen p-2 pe-lg-5 ps-lg-5 rounded-4 align-self-center">
        aaa
      </div>
    </div>
  </div>
</template>

<style setup>
.bg-chosen {
  background-color: var(--color-primary-70);
}
.bg-datalist {
  background-color: var(--color-primary-100) !important;
}
</style>