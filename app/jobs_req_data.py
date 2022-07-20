import json
import re
from collections import ChainMap
from http import client
from os import getcwd as current_path

# conn = client.HTTPSConnection('api.worldbank.org')
# conn.request("GET", "/v2/country?format=Json&per_page=299")
# response = conn.getresponse()
# data = response.read().decode()
countries = json.loads(open(
    f"{current_path()}\\json\\countriesInformations.json", "r").read())

eletricidade = json.loads(open(
    f"{current_path()}\\json\\indicadorAcessoEletricidade.json", "r").read())

analfabetismo = json.loads(open(
    f"{current_path()}\\json\\indicadorAnalfabetismo.json", "r").read())

gini = json.loads(open(
    f"{current_path()}\\json\\indicadorGini.json", "r").read())

populacao = json.loads(open(
    f"{current_path()}\\json\\indicadorPopulacao.json", "r").read())

renda = json.loads(open(
    f"{current_path()}\\json\\indicadorRenda.json", "r").read())

# page = json.loads(countries_information)[0]
result:dict = {}


#remove valores nulos dropna

if(countries[1][0]['incomeLevel']['value'] != 'Aggregate'):
    result['id'] = countries[1][0]['id']
    result['iso2Code'] = countries[1][0]['iso2Code']
    result['name'] = countries[1][0]['name']
    result['region'] = countries[1][0]['region']['value']
    result['capitalCity'] = countries[1][0]['capitalCity']
    result['longitude'] = countries[1][0]['longitude']
    result['latitude'] = countries[1][0]['latitude']
    result['incomeLevel'] = countries[1][0]['incomeLevel']['value']

aux = {
    gini[1][1]['indicator']['id']: 'giniIndex',
    populacao[1][1]['indicator']['id']: 'totalPopulation',
    analfabetismo[1][1]['indicator']['id'] : 'analfabetismo'
}
print(aux)
a={}
b={}
gini = gini[1] + populacao[1] + analfabetismo[1]



for gn in gini:
     if(gn['value']):

       if(gn['countryiso3code'] not in a.keys() ):
          a[gn["countryiso3code"]] = {aux[gn['indicator']['id']]: {'description': gn['indicator']['value'], 'data': {}}}
       elif(aux[gn['indicator']['id']] not in a[gn["countryiso3code"]].keys()):
          a[gn["countryiso3code"]][aux[gn['indicator']['id']]] = {
              'description': gn['indicator']['value'], 'data':{}}
       a[gn["countryiso3code"]][aux[gn['indicator']['id']]]['data'].update(
           {gn["date"]: gn["value"]})

y = json.dumps(a, indent=4, sort_keys=True)
file = open('teste.json', 'w')
file.write(y)
file.close()



# primeiro faz a requisição do ano corrente, se for 0 faz do ano anterior até colnseguir o ultimo ano
# se a quantidade de elementos for menor que o número da pagina, repete a rquisição enviando o total
# primeiro pega o indicador de paises, e pega os códigos, exclui os que não tem região admin, assim so pega os paises
# segundo vai pegando os outros indicadores s
# se a informação no ano corrente for null pro pais é necessário fazer uma requisição especifica para o pais com todos os anos e ver o último ano não nulo
# terceiro faz uma lista de paises e seta as bandeiras faz uma requisição grande para pegar as bandeiras
# a as bandeiras faz uma requisição grande para pegar as bandeiras
