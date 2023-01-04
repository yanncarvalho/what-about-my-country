/**
 * type of `DataIndicator`
 *
 * @typedef {array} DataIndicator
 * @property {number} year - data year
 * @property {number} value - data value
 */

/**
 * type of `IdValue`
 *
 * @typedef {object} IdValue - onject
 * @property {string} id  - Id of IdValue
 * @property {string} value - Value of IdValue
 */

/**
 * type of `Indicator`
 *
 * @typedef {object} Indicator
 * @property {string} id - Indicator id
 * @property {string} description - Indicator description
 * @property {DataIndicator} data - Indicator data
 */

/**
 * type of `Country`
 *
 * @typedef {object} Country
 * @property {string} id - Country id
 * @property {string} name - Country name
 * @property {string} capitalCity - Country capital city
 * @property {number} latitude - Country latitude
 * @property {number} longitude - Country longitude
 * @property {string} region - Country region
 * @property {string} incomeLevel - Country incomeLevel
 * @property {Array.<Indicator>} indicators  - Country indicators
 */

/**
 * type of `DataChart`
 *
 * @typedef {object} DataChart
 * @property {string} id  - DataChart id
 * @property {string} description - DataChart description
 * @property {string} labels  - DataChart labels
 * @property {Array.<DataChartDataset>} datasets - Array of datasets
 * @property {set} countryIds - Set with country ids
 */

/**
 * type of `DataChartDataset`
 *
 * @typedef {object} DataChartDataset
 * @property {string} label - DataChartDataset label
 * @property {string} borderColor - DataChartDataset borderColor
 * @property {boolean} fill - if chart value representation must be fill
 * @property {Array.<number>} data - Array of number
 */

/**
 * @constant
 * @descript object to store countryIds with hexadecimal colors, to standartize which color each country should have
 */
const COUNTRY_COLOR = new Object();

/**
 * @description scroll to element with the given id, if the element exists
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
 * @description Convert an Object with attribute "key" into a string
 * @param {object} obj an object with attribute "key"
 */
export function stringifyKeyObj(obj) {
  const regex = /"/g;
  let keys = Object.values(obj).map((o) => o.key) ?? [];
  return JSON.stringify(keys).replace(regex, "");
}

/**
 * @description convert an indicator to a datachart
 * @param {Array.<IdValue>} indicatorIdValue indicatorIdValue to be converted
 * @returns {DataChart} dataChart from an indicator
 */
function convIndiToDataChart(indicatorIdValue) {
  return indicatorIdValue.reduce(
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
 * @param {Array.<Country>} countries countries
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
