import asyncio
from logging import info
from threading import Thread

from .api.models_country import Country

class Populate(Thread):
  is_population = False

  def run(self):
    if not Populate.is_population:
     Populate.is_population = True
     keys = Country.all_keys_from_net()
     asyncio.run(Populate.countries(keys))
     Populate.is_population = False

  @staticmethod
  async def countries(keys: set):
      requests_async = [Country.save_from_net(key) for key in keys]
      await asyncio.gather(*requests_async)
      Populate.is_population = False
