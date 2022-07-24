from django.http import HttpResponse
from django.shortcuts import render

from backend.api.models_country import Country

def index(request):
  return HttpResponse(Country.all_keys())


# VER O SUPER
# AJEITAR O PADRÃO DE HELPER
# CONFIGURAR PARA SETAR AS CHAVES
# CRIAR O ENDPOINT QUE PEGA UMA SÓ REQUISIÇÃO
