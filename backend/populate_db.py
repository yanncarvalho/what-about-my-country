import asyncio
from logging import info
from threading import Thread

from .api.models_country import Country

class Populate(Thread):
  def run(self):
    keys = list(Country.all_keys_from_net())
    asyncio.run(Populate.countries(keys))

  @staticmethod
  async def countries(keys: list):
      requests_async = [Country.save_from_net(key) for key in keys]
      await asyncio.gather(*requests_async)
