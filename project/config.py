# -*- coding: utf-8 -*-

#=------------- APPLICATION SETTINGS --------------=#
DEBUG: bool = True

CSRF_ENABLED: bool = True


#=---------------- WORLD BANK API -----------------=#
WB_INDICATOR_KEY_API_VALUE_DICT: dict = {
    # api-key : dict-key
    'NY.GDP.MKTP.CD': 'GDP',
    'SP.POP.TOTL': 'totalPopulation',
    'SE.ADT.1524.LT.ZS': 'literacyRate',
    'SI.POV.GINI': 'giniIndex',
    'EG.ELC.ACCS.ZS': 'eletricityAccess'
}

WB_API_ROOT_URL: str = 'api.worldbank.org'

WB_API_VERSION: str = 'v2'

WB_COUNTRIES_INFO_URL: str = WB_API_VERSION+'/'+'country'+'/'

WB_INDICATOR_URL: str = WB_COUNTRIES_INFO_URL+'indicator'+'/'

#=---------------- REDIS INFO -----------------=#
COUNTRIES_BASIC_INFO_FIELD: str = 'basicInfo'

COUNTRIES_FIELDS = set(WB_INDICATOR_KEY_API_VALUE_DICT.values()).union({COUNTRIES_BASIC_INFO_FIELD})