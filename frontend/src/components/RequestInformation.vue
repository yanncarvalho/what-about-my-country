<script setup>
import { reactive, ref, watch } from "vue";
import RequestInformationDatalist from "./RequestInformationDatalist.vue";
import RequestInformationButton from "./RequestInformationButton.vue";
const selectedTags = reactive({
  country: [],
  indicator: [],
});

const hasBtnDisabled = ref(true);

const emit = defineEmits(["onResult"]);

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
  <form action="javascript:void(0);">
    <RequestInformationDatalist
      @selectedElements="
        (v) => {
          selectedTags.country = v;
        }
      "
      label="Country"
      placeholder="Choose a Country"
      graphQLEnumName="Code"
      :isDropDown="true"
      :maxResult="6"
    />
    <RequestInformationDatalist
      @selectedElements="
        (v) => {
          selectedTags.indicator = v;
        }
      "
      label="Indicator"
      placeholder="Choose an Indicator"
      graphQLEnumName="IndicatorId"
      :alwaysShowOptions="true"
    />
    <RequestInformationButton
      :disabled="selectedTags.country.length === 0 || hasBtnDisabled"
      @click="bindData"
      value="Show me these countries"
      ariaLabel="Click to show information about selected countries"
    />
  </form>
</template>
