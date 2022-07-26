from logging import info

from .api.models_country import Country


def countries():
  countries = Country.all_countries_from_net()
  for country in countries:
    country.save()



