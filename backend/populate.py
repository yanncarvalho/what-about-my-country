import asyncio
from ast import List
from threading import Thread
from typing import Coroutine, Set

from .api.models_country import Country


class Populate(Thread):

  _is_population: bool = False

  def run(self):

    if Populate._is_population is False:
     Populate._is_population = True
     self.start_populations()
     Populate._is_population = False

  @staticmethod
  def start_countries():

    async def countries(keys: Set[str]):
      requests_async: List[Coroutine] = \
        [Country.save_from_net(key) for key in keys]
      await asyncio.gather(*requests_async)
      Populate._is_population = False

    keys = Country.all_keys_from_net()
    asyncio.run(countries(keys))

  def start_populations(self):

    Populate.start_countries()





