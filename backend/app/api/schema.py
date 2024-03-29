"""GraphQL schemas"""
import asyncio
from typing import Dict, List, Tuple
from ariadne import ObjectType, SchemaDirectiveVisitor, make_executable_schema
from django.conf import settings as conf
from graphql import GraphQLError, default_field_resolver
from .models import Field
from .models_country import Country


def _from_tuple_to_str_enum(value: Tuple[Dict[str, str]]) -> str:
    """ convert a tuple of dictionary with keys id and name to a graphql enum with description

    Args:
    - value: Tuple of dictionary with keys id and name that will be converted into a String

    Returns:
      String converted
    """
    resp: str = "{"
    for val in value:
        aux = f"\"{val['name']}\"{val['id']}"
        resp += aux
    resp += "}"
    return resp


__fields: Dict[str, str] = dict(conf.FROM_NET_KEY_TO_DICT_VALUE)
__fields.pop(conf.API_BASIC_INFO_URL, None)
__fields_id: Tuple[Dict[str, str]] = tuple(__fields.values())
indicators_id: str = _from_tuple_to_str_enum(__fields_id)
country_codes: str = _from_tuple_to_str_enum(Country.all_keys_n_name_from_net())

schema_graphql = '''
    directive @zeroOrPositive on ARGUMENT_DEFINITION

    type Query {
        "country request - code in iso2Code"
        country(codes: [Code!]!): [Country!]
    }

    """
    Get some information about a particular country from [World Bank API] (https://data.worldbank.org/)
    """
    type Country {
        "id in iso2Code"
        id: String!

        "country name"
        name: String!

        "country region"
        region: String!

        "country capital city"
        capitalCity: String!

        "country longitude"
        longitude: Float!

        "country latitude"
        latitude: Float!

        "country [income level] (https://en.wikipedia.org/wiki/List_of_countries_by_GNI_(nominal)_per_capita)"
        incomeLevel: String!

        "country indicators"
        indicators(ids:[IndicatorId!]!): [Indicator!]
    }

    """
    Country Indicator from [World Bank API] (https://data.worldbank.org/)
    """
    type Indicator{
        "Indicator id"
        id: String!

        "indicator description"
        description: String!

        "indicator data, by default return all data, but it is possible to set minimum year"
        data (minYear: Int! = 0 @zeroOrPositive): [Data!]
    }

    """
    Indicator data with year and its respective value
    """
    type Data{
        "Data year"
        year: Int!

        "Data value"
        value: Float!
    }

''' + f'''
    """
    Enumerator with all possible country indicators
    """
    enum IndicatorId {indicators_id}

    """
    Country [iso2Code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
    """
    enum Code {country_codes}
'''

query = ObjectType('Query')


@query.field('country')
def _resolve_country(*_, codes):
    """ GraphQL Query country resolve
      Args:
      - code: country iso2Code id

      Returns:
          List of country fields
    """
    fields_list: List[Field] = []
    for code in codes:
        countries = Country(code)
        if countries.is_empty():
            asyncio.run(countries.save_from_net(code))
        fields = countries.get_fields()
        fields_list.append(fields)
    return fields_list


country = ObjectType('Country')


@country.field('id')
@country.field('incomeLevel')
@country.field('latitude')
@country.field('longitude')
@country.field('capitalCity')
@country.field('region')
@country.field('name')
def _resolve_country_elements(fields, info):
    """ GraphQL type country elements resolve

      Args:
      - fields: list of fields
      - info: information about GraphQL request

      Returns:
        Requested field element
    """
    value = info.field_name
    key: Dict[str, str] = conf.FROM_NET_KEY_TO_DICT_VALUE[conf.API_BASIC_INFO_URL]
    field: Field = fields[key['id']]
    return field.info[value]


@country.field('indicators')
def _resolve_indicators(indicators, _, ids):
    """ GraphQL type country indicators resolve

      Args:
      - indicators: list of indicators
      - id: list of requested indicators id

      Returns:
        Requested indicators element
    """
    indicators_filtered = [indicators[i] for i in ids if i in indicators.keys()]
    return indicators_filtered


indicator = ObjectType('Indicator')


@indicator.field('description')
@indicator.field('id')
def _resolve_indicator(indicartor, info):
    """ GraphQL Type indicators resolve

      Args:
      - indicator: information indicator
      - info: information about graphql request

      Returns:
       requested indicator element
    """
    value = info.field_name
    return indicartor.info[value]


@indicator.field('data')
# pylint: disable=invalid-name
def _resolve_data(indicators, _, minYear: int):
    """ GraphQL Type data resolve

      Args:
      - indicators: information indicator
      - minYear: minimum year for response

      Returns:
       data filtered by minimum year
    """
    data_filtered = [date for date in indicators.info['data']
                     if date['year'] >= minYear]
    return data_filtered


data = ObjectType('Data')


@data.field('value')
@data.field('year')
# pylint: disable=redefined-outer-name
def _resolve_data_elements(data, info):
    """ GraphQL Type data resolver

      Args:
      - data: data elements
      - info: information about graphql request

      Returns:
       Requested data element
    """
    value = info.field_name
    return data[value]


def format_error(error: GraphQLError, *_) -> dict:
    """GraphQL formatter error"""
    formatted = error.formatted
    formatted.pop('path', None)
    return formatted


class ZeroOrPositiveDirective(SchemaDirectiveVisitor):
    """ZeroOrPositiveDirective sets GraphQL directive to @zeroOrPositive"""

    def visit_argument_definition(self, argument, field, _):
        original_resolver = field.resolve or default_field_resolver

        def resolve_or_raise_error_if_negative(obj, info,  **kwargs):
            for key, val in kwargs.items():
                if val < 0:
                    raise ValueError(f"{key} has to be equal zero or positive")
            return original_resolver(obj, info, **kwargs)

        field.resolve = resolve_or_raise_error_if_negative
        return argument


schema = make_executable_schema(
    schema_graphql, query, country, indicator, data,
    directives={'zeroOrPositive': ZeroOrPositiveDirective})
