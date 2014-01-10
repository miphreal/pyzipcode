from collections import namedtuple
from pony.orm import ObjectNotFound, db_session
from .model import ZipCodeModel

zc_keys = ('zip_number', 'city', 'state', 'country', 'latitude', 'longitude', 'timezone')
ZipCode = namedtuple('ZipCode', zc_keys)


class ZipNotFoundError(Exception):
    pass


class ZipCodeDatabase(object):
    def _prepare_result(self, obj):
        return ZipCode(*[getattr(obj, k) for k in zc_keys])

    @db_session
    def get_zipcodes_around_radius(self, zip_number, radius):
        zip_number = self.get(zip_number)
        radius = float(radius)

        lng_min, lng_max = zip_number.longitude - (radius / 69.0), zip_number.longitude + (radius / 69.0)
        lat_min, lat_max = zip_number.latitude - (radius / 49.0), zip_number.latitude + (radius / 49.0)
        return map(
            self._prepare_result,
            ZipCodeModel.select(lambda z: lng_min <= z.longitude and z.longitude <= lng_max and \
                                          lat_min <= z.latitude and z.latitude <= lat_max)
        )

    @db_session
    def find_zip(self, city=None, state=None, limit=None):
        query = None
        if state and city:
            query = lambda z: z.city == city and z.state == state
        elif state:
            query = lambda z: z.state == state
        elif city:
            query = lambda z: z.city == city

        zip_codes = ZipCodeModel.select(*((query,) if query else ()))
        if limit:
            return map(self._prepare_result, zip_codes[:limit])
        return map(self._prepare_result, zip_codes)

    @db_session
    def get(self, zip_number):
        try:
            return self._prepare_result(ZipCodeModel[str(zip_number)])
        except ObjectNotFound as e:
            raise ZipNotFoundError(e.message)

    def __getitem__(self, zip_number):
        return self.get(zip_number)

