from decimal import Decimal
from pony.orm import Database, PrimaryKey, Required, Optional, sql_debug

from .conf import db_settings


db = Database(db_settings['db_engine'], db_settings['db_location'], create_db=True)


class ZipCodeModel(db.Entity):
    zip_number = PrimaryKey(unicode, 10)
    city = Required(unicode)
    state = Required(unicode)
    country = Required(unicode)
    latitude = Optional(float)
    longitude = Optional(float)
    timezone = Optional(unicode)


sql_debug(db_settings['debug'])
db.generate_mapping(create_tables=True)
