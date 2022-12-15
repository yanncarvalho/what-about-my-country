/**
 * type of `DataIndicator`
 *
 * @typedef {array} DataIndicator
 * @property {number} year
 * @property {number} value
 */

/**
 * type of `IdValue`
 *
 * @typedef {object} IdValue
 * @property {string} id
 * @property {string} value
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
 * @constant
 * @descript object to store countryIds with hexadecimal colors, to standartize which color each country should have
 */
const COUNTRY_COLOR = new Object();

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
 * @returns {string} an String with color in hexadecimal
 */
export function genHexDecimalColor() {
  let n = (Math.random() * 0xfffff * 1000000).toString(16);
  return "#" + n.slice(0, 6);
}

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
 * @param {[IdValue]} indicatorIdValue indicatorIdValue to be converted
 * @returns {DataChart} dataChart from an indicator
 */
function convIndiToDataChart(indicatorIdValue) {
  return indicatorIdValue.reduce(
    (o, item) => ({
      ...o,
      [item.id]: new Object({
        id: item.id,
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
 * @description convert Country into an arrat of indicator IdValue
 * @param {[Country]} countries country information
 * @returns {[IdValue]} indicators IdValue
 */
function convCountryToIndiIdValue(countries) {
  return countries
    .flatMap((country) => country.indicators)
    .map((indi) => {
      return { id: indi.id, value: indi.description };
    });
}

/**
 * @description generate indicator chart parameters
 * @param {[Country]} countries country information
 * @returns {DataChart} dataChart from an indicator
 */
export function genChartsIndicator(countries) {
  const indicatorIdValue = convCountryToIndiIdValue(countries);
  const chartIndi = convIndiToDataChart(indicatorIdValue);
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
      if (!COUNTRY_COLOR[country.id]) {
        COUNTRY_COLOR[country.id] = genHexDecimalColor();
      }
      chartIndi[indi.id].countryIds.add(country.id);
      chartIndi[indi.id].labels = indiLabel;
      chartIndi[indi.id].datasets.push({
        data: chartData,
        label: country.name,
        borderColor: COUNTRY_COLOR[country.id],
        fill: false,
      });
    }
  }
  return chartIndi;
}
