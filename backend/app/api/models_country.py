"""Country model"""
import asyncio
import logging
from typing import Dict, List, Tuple, Optional, Coroutine, Set
import threading
from app.api import helpers, models

class Country:
    """Country class represeting database data and World Bank API."""
    _REDIS_COUNTRIES_ID: str = 'api:country:iso2Code'
    _is_populating: bool = False

    def __init__(self, country_code: str):
        """Inits Country with country iso2Code id."""
        key: str = ':'.join(
            (Country._REDIS_COUNTRIES_ID, country_code.upper()))
        Country._database = models.RedisModel(key=key)

    def get_fields(self) -> Dict[str, models.Field]:
        """get information from the database"""
        return Country._database.get_fields()

    def is_empty(self) -> bool:
        """check if a country in the database has fields"""
        return not bool(Country._database.get_fields())

    @classmethod
    async def save_from_net(cls, country_code: str) -> None:
        """save a country with its iso2Code id from World Bank API in the database."""
        from_net: Optional[helpers.CountryAPIRequest] = await helpers.get_from_net(country_code)
        from_net_fields: List[models.Field] = \
            [models.Field(k, v) for k, v in from_net.items()]
        cls(country_code)._database.save(from_net_fields)
        Country.trigger_save_all_countries().start()

    @staticmethod
    def all_keys_n_name_from_net() -> Tuple[Dict[str, str]]:
        """
        get a tuple of dictionaries with iso2Code
        id (key = id) and country name (key = name) from World Bank API
        """
        return helpers.get_keys_n_name_from_net()

    @staticmethod
    def del_all_countries() -> None:
        """delete all countries from the database"""
        models.RedisModel.del_keys_by_pattern(Country._REDIS_COUNTRIES_ID)

    @staticmethod
    def trigger_save_all_countries():
        """return a thread class with save all countries redis method"""
        return threading.Thread(
            target=Country.save_all_countries,
            daemon=True)


    @staticmethod
    def save_all_countries() -> None:
        """save all countries in the database"""
        if Country._is_populating is False:
            Country._is_populating = True
            logging.info('start population')
            keys: Set[str] = set(val['id']
                             for val in Country.all_keys_n_name_from_net())
            try:
                async def async_countries(keys: Set[str]):
                    requests_async: List[Coroutine] = \
                        [Country.save_from_net(key) for key in keys]
                    return await asyncio.gather(*requests_async)
                asyncio.run(async_countries(keys))
                Country._is_populating = False
            except RuntimeError as err:
                logging.error(
                "Could not save all countries in the database: %s", err)
