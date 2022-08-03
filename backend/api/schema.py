import asyncio
from typing import Dict, List, Set

from ariadne import ObjectType, SchemaDirectiveVisitor, make_executable_schema
from django.conf import settings as conf
from graphql import GraphQLError, default_field_resolver

from .models import Field
from .models_country import Country


def _from_set_to_str_enum(value: set) -> str:
    return str(value).replace("'", "")


__fields: Dict[str, str] = dict(conf.FROM_NET_KEY_TO_DICT_VALUE)
__fields.pop(conf.API_BASIC_INFO_URL, None)
__fields_id: Set[str] = set(__fields.values())

schema_graphql = '''

    directive @zeroOrPositive on ARGUMENT_DEFINITION

    type Query {
        country(code: [Codes!]!): [Country!]
    }

    type Country {
        id: String!
        name: String!
        region: String!
        capitalCity: String!
        longitude: Float!
        latitude: Float!
        incomeLevel: String!
        indicators(id:[IndicatorsId!]!): [Indicator!]
    }

    type Indicator{
        id: String!
        description: String!
        data (minYear: Int! = 0 @zeroOrPositive): [Data!]
    }

    type Data{
        year: Int!
        value: Float!
    }

''' + '''
    enum IndicatorsId {fields}
    enum Codes {codes_enum}
'''.format(
    fields=_from_set_to_str_enum(
      __fields_id),
    codes_enum=_from_set_to_str_enum(Country.all_keys_from_net()))

query = ObjectType('Query')


@query.field('country')
def _resolve_country(*_, code):
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
    value = info.field_name
    field: Field = fields[conf.FROM_NET_KEY_TO_DICT_VALUE[conf.API_BASIC_INFO_URL]]
    return field.info[value]

@country.field('indicators')
def _resolve_indicators(indicators, _, id):
    indicators_filtered = [indicators[i] for i in id if i in indicators.keys()]
    return indicators_filtered

indicator = ObjectType('Indicator')

@indicator.field('description')
@indicator.field('id')
def _resolve_indicator(indicartor, info):
    value = info.field_name
    return indicartor.info[value]


@indicator.field('data')
def _resolve_data(indicators, _, minYear: int):
    data_filtered = [date for date in indicators.info['data']
                     if date['year'] >= minYear]
    return data_filtered


data = ObjectType('Data')


@data.field('value')
@data.field('year')
def _resolve_data_elements(data, info):
    value = info.field_name
    return data[value]


def format_error(error: GraphQLError, *_) -> dict:

    formatted = error.formatted
    formatted.pop('path', None)
    return formatted


class ZeroOrPositiveDirective(SchemaDirectiveVisitor):

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
