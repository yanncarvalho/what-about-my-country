import asyncio
import logging
from threading import Thread
from typing import Coroutine, List, Set
from .models_country import Country

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
  def start_countries() -> None:
    """start the country Population"""

    keys: Set[str] =  set( val['id'] for val in Country.all_keys_n_name_from_net())
    try:
      async def async_countries(keys: Set[str]):
       requests_async: List[Coroutine] = \
        [Country.save_from_net(key) for key in keys]
       return await asyncio.gather(*requests_async)

      asyncio.run(async_countries(keys))
    except Exception as e:
     logging.error("Could not populate database with countries information", e)

  def start_populations(self) -> None:
    """start the population itself"""
    logging.info('database population has been started')
    Populate.start_countries()

