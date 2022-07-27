from backend.api import helpers
from django.http import HttpResponse
from django.shortcuts import render
from backend.api.models_country import Country

def index(request):
  return HttpResponse(  Country("BR").get_fields())
