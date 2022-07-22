# -*- coding: utf-8 -*-
import re

import project.db as db
import helpers
import initialize
import project.helpers_convertors as conv
from config import *
from project.models import Country, Field

def get_country_field(iso2code: str, field_id: str) -> Field:
  return db.get_country_field(iso2code, field_id)

def get_country(iso2code: str) -> Country:
  return db.get_country(iso2code)

def set_country_field(iso2code: str, field: Field) -> Country:
  return db.set_country_field(iso2code, field)

def get_countries_ids() -> list:
  '''se não tiver ja coloca'''
  keys = db.get_countries_ids()
  if(len(keys) == 0):
    initialize.create_country_fields_db()
    keys = db.get_countries_ids()
  return keys

