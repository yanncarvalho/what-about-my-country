from backend.api import helpers
from django.http import HttpResponse
from django.shortcuts import render
from backend.api.models_country import Country

def index(request):

  return HttpResponse(Country.get_from_internet('BR'))

#toda vez que não encontrar um dado = buscar na net
#TODO fazer endpoints
#TODO colocar graphql