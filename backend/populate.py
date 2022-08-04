import asyncio
from ast import List
from threading import Thread
from typing import Coroutine, Set

from .api.models_country import Country


class Populate(Thread):
  """Populate class implemention methods to populate the database"""
  _is_population: bool = False

  def run(self):
    """start the population database of if process was not running"""
    if Populate._is_population is False:
     Populate._is_population = True
     self.start_populations()
     Populate._is_population = False

  @staticmethod
  def start_countries():
    """start the country Pppulation"""
    async def countries(keys: Set[str]):
      """populate database with information from all countries"""
      requests_async: List[Coroutine] = \
        [Country.save_from_net(key) for key in keys]
      await asyncio.gather(*requests_async)
      Populate._is_population = False

    keys = Country.all_keys_from_net()
    asyncio.run(countries(keys))

  def start_populations(self):
    """start the population itself"""
    Populate.start_countries()





