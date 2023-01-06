/**
 * @description query to select country information
 * @param {string} codes country codes
 * @param {string} ids indicitors ids
 * @returns {string} graphQl query
 */
export const selectCountries = (codes, ids) =>
  ` {
    country(codes:  ${codes} ) {
      id,
      name,
      capitalCity,
      latitude,
      longitude,
      region,
      incomeLevel,
      indicators(ids: ${ids}) {
        id
        description,
        data{
              value,
              year
        }
      }
    }
   }
`;

/**
 * @description query to instropect graphql enumValues
 * @param {string} enumName enumValues name
 * @returns {string} graphQl query
 */
export const instropectEnumValue = (enumName) => `
  {
    __type(name: "${enumName}") {
      enumValues {
        name
        description
      }
    }
  }
`;
