from http.client import responses
import json
import re
from os import getcwd as current_path

import time
#TODO colocar a requisição para ser feita - a primeira per_page = 1, ai pega o total e o lastupdate
#TODO separar as coisas deste escript em outros arquivos
#TODO configurar o redis, o acesso
#TODO setar informações no redis
#TODO criar rotina que baixa os sgv
#TODO criar rotina que é executada dado uma periodicidade - para poder atualizar as bandeiras e as infos
#TODO criar o endpoint
#TODO implementar o GRAPHQL


def current_milli_time():
    return round(time.time() * 1000)
inicial = current_milli_time()

def _sanitize_string(str:str) -> str:
    """
    Remove unnecessary caracteries or change words
    """
    str = str.strip()

    rule = lambda st: re.sub('\s*[SAR]*\s*,.*', '', st)

    exceptions = {
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Congo, Rep.": "Republic of the Congo",
        "Korea, Dem. People's Rep.": "North Korea",
        "Korea, Rep.": "South Korea",
        "Bahamas, The": "The Bahamas",
        "Population, total" : "Total population",
        "Lao PDR": "Laos",
        "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
        "St. Lucia": "Saint Lucia",
        "St. Kitts and Nevis": "Saint Kitts and Nevis"
    }

    return exceptions[str] if str in exceptions.keys() else rule(str)


# conn = client.HTTPSConnection('api.worldbank.org')
# conn.request("GET", "/v2/country?format=Json&per_page=299")
# response = conn.getresponse()
# data = response.read().decode()
countries = json.loads(open(
    f"{current_path()}/json/countriesInformations.json", "r").read())

eletricidade = json.loads(open(
    f"{current_path()}/json/indicadorAcessoEletricidade.json", "r").read())

literacy_rate = json.loads(open(
    f"{current_path()}/json/indicadorAlfabetizacao.json", "r").read())

gini = json.loads(open(
    f"{current_path()}/json/indicadorGini.json", "r").read())

populacao = json.loads(open(
    f"{current_path()}/json/indicadorPopulacao.json", "r").read())

renda = json.loads(open(
    f"{current_path()}/json/indicadorRenda.json", "r").read())


result:dict = {}


aux = {
    gini[1][1]['indicator']['id']: 'giniIndex',
    populacao[1][1]['indicator']['id']: 'totalPopulation',
    literacy_rate[1][1]['indicator']['id']: 'literacyRate',
    renda[1][1]['indicator']['id']: 'GDP',
    eletricidade[1][1]['indicator']['id']: 'eletricityAccess'
}

result:dict = {}
responses = populacao[1]+eletricidade[1]+renda[1]+gini[1]+literacy_rate[1]

for resp in responses:
     value = resp['value']
     if(value != None):
       country_code = resp['countryiso3code']
       description = _sanitize_string(resp['indicator']['value'])
       indicator = aux[resp['indicator']['id']]

       if(country_code not in result.keys()):
          result[country_code] = {}

       if(indicator not in result[country_code].keys()):
           result[country_code].update(
                                        {
                                            indicator: {
                                                 'description': description,
                                                 'data': {}
                                            }
                                        }
                                      )
       result[country_code][indicator]['data'].update({resp['date']: value})


for info in countries[1]:
    if(info['incomeLevel']['value'] != 'Aggregates' and info['longitude'] != ''):
        jsn = {
            'id' : info['id'],
            'iso2Code': info['iso2Code'],
            'name': _sanitize_string(info['name']),
            'region': _sanitize_string(info['region']['value']),
            'capitalCity': _sanitize_string(info['capitalCity']),
            'longitude': float(info['longitude']),
            'latitude': float(info['latitude']),
            'incomeLevel': _sanitize_string(info['incomeLevel']['value']),
        }

        if(jsn['id'] in result.keys()):
            jsn.update(result[jsn['id']])
        #TODO colocar log para saber que um tipo nao foi convertido
        archive = json.dumps(jsn, indent=4)
        file = open(f'/home/yann/what-about-my-country/app/final/{jsn["name"]}.json', 'w')
        file.write(archive)
        file.close()
print(current_milli_time()-inicial)