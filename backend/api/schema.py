import asyncio
from typing import Dict, List, Set
from ariadne import ObjectType, SchemaDirectiveVisitor, make_executable_schema
from django.conf import settings as conf
from graphql import GraphQLError, default_field_resolver
from .models import Field
from .models_country import Country


def _from_set_to_str_enum(value: set) -> str:
    """ convert a set to a String

    Args:
    - value: Set that will be converted into a String

    Returns:
      Set to a String by removing apostrophes
    """
    return str(value).replace("'", "")


__fields: Dict[str, str] = dict(conf.FROM_NET_KEY_TO_DICT_VALUE)
__fields.pop(conf.API_BASIC_INFO_URL, None)
__fields_id: Set[str] = set(__fields.values())

schema_graphql = '''
    directive @zeroOrPositive on ARGUMENT_DEFINITION

    type Query {
        "country request - code in iso3code"
        country(code: [Codes!]!): [Country!]
    }

    """
    Get some information about a particular country from [World Bank API] (https://data.worldbank.org/)
    """
    type Country {
        "id in iso3code"
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
        indicators(id:[IndicatorsId!]!): [Indicator!]
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

''' + '''
    """
    Enumerator with all possible country indicators
    """
    enum IndicatorsId {fields}

    """
    Country [iso3Code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)
    """
    enum Codes {codes_enum}
'''.format(
    fields=_from_set_to_str_enum(
      __fields_id),  # dynamic field formatting for graphql request
    codes_enum=_from_set_to_str_enum(Country.all_keys_from_net()))  # dynamic country id  formatting for graphql request

query = ObjectType('Query')


@query.field('country')
def _resolve_country(*_, code):
    """ GraphQL Query country resolve
      Args:
      - code: country iso3code id

      Returns:
          List of country fields
    """
    fields_list: List[Field] = []
    for cd in code:
        country = Country(cd)
        if(country.is_empty()):
            asyncio.run(country.save_from_net(cd))
        fields = country.get_fields()
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
    field: Field = fields[conf.FROM_NET_KEY_TO_DICT_VALUE[conf.API_BASIC_INFO_URL]]
    return field.info[value]

@country.field('indicators')
def _resolve_indicators(indicators, _, id):
    """ GraphQL type country indicators resolve

      Args:
      - indicators: list of indicators
      - id: list of requested indicators id

      Returns:
        Requested indicators element
    """
    indicators_filtered = [indicators[i] for i in id if i in indicators.keys()]
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
