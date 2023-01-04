<template>
  <svg
    id="logo-text"
    height="74px"
    width="750px"
    class="svg-resize"
    aria-labelledby="textTitle"
    role="img"
  >
    <title id="textTitle">What about my country?</title>
    <text x="5" y="55" class="title-format">WHAT ABOUT</text>
    <text x="370" y="55" class="title-format subtitle-move">MY COUNTRY?</text>
  </svg>
</template>

<style setup>
.title-format {
  font: 45pt var(--font-title);
  fill: #d9d9d9;
  letter-spacing: -6px;
  stroke: black;
  stroke-width: 7px;
  paint-order: markers stroke fill;
}

@media screen and (max-width: 880px) {
  .title-format {
    font-size: 27pt;
    letter-spacing: -4px;
    transform: translate(0px, -10px);
  }

  .svg-resize {
    height: 60px;
    width: 449px;
  }

  .subtitle-move {
    transform: translate(-145px, -10px);
  }
}

@media screen and (max-width: 453px) {
  .title-format {
    font-size: 26pt;
    letter-spacing: -2px;
    transform: translate(5px, -20px);
  }

  .subtitle-move {
    transform: translate(-360px, 10px);
  }

  .svg-resize {
    height: 70px;
    width: 245px;
  }
}
</style>
