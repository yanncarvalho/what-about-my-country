import asyncio
from ariadne import ObjectType, make_executable_schema
from django.conf import settings as conf
from .models import Field
from .models_country import Country

def _from_set_to_str_enum (val: set) -> str:
   return str(val).replace("'", "")

__fields_id  = set(conf.FROM_NET_KEY_TO_FIELD_VALUE.values())

type_defs = """
    type Query {
        country(code: [Codes!]!): [Country]
    }

    type Country {
        id: String
        name: String,
        region: String,
        capitalCity: String,
        longitude: Float,
        latitude: Float,
        incomeLevel: String,
        fields(id:[Fields!]!): [Field]
    }

    type Field{
        id: String,
        description: String,
        data (minYear: Int!): [Data]
    }

    type Data{
        year: Int!
        value: Float!
    }
""" + """
    enum Fields {fields}
    enum Codes {codes_enum}
""".format(fields = _from_set_to_str_enum(__fields_id),
           codes_enum = _from_set_to_str_enum(Country.all_keys_from_net()))

query = ObjectType('Query')

@query.field('country')
def resolve_country(*_, code):
    fields_list: list = []
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
def resolve_country(fields,  info):
    value = info.field_name
    field: Field = fields[conf.BASIC_INFO_FIELD]
    return field.info[value]

@country.field('fields')
def resolve_fields(obj, _, id):
    fiedls_filtered = [ obj[i] for i in id if i in obj.keys() ]
    return fiedls_filtered

field = ObjectType('Field')

@field.field('description')
@field.field('id')
def resolve_description(field, info):
    value = info.field_name
    return field.info[value]

@field.field('data')
def resolve_data(fields, _, minYear:int):
   if minYear < 0:
    raise ValueError("only positive numbers are allowed")
   else:
    data_filtered = [ date for date in fields.info['data']
                      if date['year'] >= minYear ]
   return data_filtered

data = ObjectType('Data')

@data.field('value')
@data.field('year')
def resolve_year(data, info):
    value = info.field_name
    return data[value]

schema = make_executable_schema(type_defs, query, country, field, data)