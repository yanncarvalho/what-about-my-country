/**
 * type of `DataIndicator`
 *
 * @typedef {array} DataIndicator
 * @property {number} year
 * @property {number} value
 */

/**
 * type of `Indicator`
 *
 * @typedef {object} Indicator
 * @property {string} id
 * @property {string} description
 * @property {DataIndicator} data
 */

/**
 * type of `Country`
 *
 * @typedef {object} Country
 * @property {string} id
 * @property {string} name
 * @property {string} capitalCity
 * @property {number} latitude
 * @property {number} longitude
 * @property {string} region
 * @property {string} incomeLevel
 * @property {[Indicator]} indicators
 */

/**
 * type of `DataChart`
 *
 * @typedef {object} DataChart
 * @property {string} id
 * @property {string} description
 * @property {string} labels
 * @property {[DataChartDataset]} datasets
 * @property {set} countryIds
 */

/**
 * type of `DataChartDataset`
 *
 * @typedef {object} DataChartDataset
 * @property {string} label
 * @property {string} borderColor
 * @property {boolean} fill
 * @property {[number]} data
 */

/**
 * @description scroll to element with the id informed if the element exists
 * @param {string} id element Id
 */
export function scrollToId(id) {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
}

/**
 * @description Generate a random hexadecimal color
 *
 * @returns {string} an String with color in hexadecimal
 */
const genRandomColor = () =>
  "#" + Math.floor(Math.random() * 16777215).toString(16);

/**
 * @description Convert an Object with in its values an attribute "key" into a string
 * @param {object} obj an object with in its values
 */
export function stringifyKeyObj(obj) {
  const regex = /"/g;
  let keys = Object.values(obj).map((o) => o.key) ?? [];
  return JSON.stringify(keys).replace(regex, "");
}

/**
 * @description convert an indicator in a datachart
 * @param {Indicator} indicator indicator to be converted
 * @returns { DataChart} dataChart from an indicator
 */
function convIndiToDataChart(indicator) {
  return indicator.reduce(
    (o, item) => ({
      ...o,
      [item.key]: new Object({
        id: item.key,
        description: item.value,
        labels: new Array(),
        datasets: new Array(),
        countryIds: new Set(),
      }),
    }),
    {}
  );
}
/**
 * @description generate indicator chart parameters
 * @param {Indicator} indicator indicator
 * @param {[Country]} countries countries
 * @returns { DataChart} dataChart from an indicator
 */
export function genChartsIndicator(indicator, countries) {
  const chartIndi = convIndiToDataChart(indicator);
  for (let country of countries) {
    for (let indi of country.indicators) {
      const indiData = indi.data.reduce(
        (a, v) => ({ ...a, [v.year]: v.value }),
        {}
      );
      const indiDataYears = Object.keys(indiData);
      const indiLabel = indiDataYears
        .concat(
          chartIndi[indi.id].labels.filter((y) => !indiDataYears.includes(y))
        )
        .sort((a, b) => a - b);

      const chartData = indiLabel.map((l) => indiData[l] ?? NaN);

      chartIndi[indi.id].countryIds.add(country.id);
      chartIndi[indi.id].labels = indiLabel;
      chartIndi[indi.id].datasets.push({
        data: chartData,
        label: country.name,
        borderColor: genRandomColor(),
        fill: false,
      });
    }
  }
  return chartIndi;
}
