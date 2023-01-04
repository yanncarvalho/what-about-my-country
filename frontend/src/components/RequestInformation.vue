<script setup>
import { reactive, ref, watch } from "vue";
import Button from "./ButtonComponent.vue";
import RequestInformationDatalist from "./RequestInformationDatalist.vue";

const selectedTags = reactive({
  country: [],
  indicator: [],
});
const hasBtnDisabled = ref(true);
const emit = defineEmits(["onResult"]);

/**
 * @description action when click button
 */
function bindData() {
  let result = JSON.parse(JSON.stringify(selectedTags));
  emit("onResult", result);
  hasBtnDisabled.value = true;
}

watch(selectedTags, () => {
  if (hasBtnDisabled.value) {
    hasBtnDisabled.value = false;
  }
});
</script>

<template>
  <form action="javascript:void(0);" id="form-datalists">
    <RequestInformationDatalist
      @selectedElements="selectedTags.country = $event"
      label="Country"
      placeholder="Choose a Country"
      data-cy="datalistCountry"
      id="datalistCountry"
      graphQLEnumName="Code"
      :isDropDown="true"
      :maxResult="6"
    />
    <RequestInformationDatalist
      @selectedElements="selectedTags.indicator = $event"
      label="Indicator"
      placeholder="Choose an Indicator"
      data-cy="datalistIndicator"
      graphQLEnumName="IndicatorId"
      id="datalistIndicator"
      :alwaysShowOptions="true"
    />
    <div class="d-flex container justify-content-center">
      <Button
        data-cy="showCountriesBtn"
        typeBtn="submit"
        id="showCountriesBtn"
        :disabled="selectedTags.country.length === 0 || hasBtnDisabled"
        @click="bindData"
        value="Show me these countries"
        ariaLabel="Click to show information about selected countries"
      />
    </div>
  </form>
</template>
