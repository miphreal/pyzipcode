import unittest
import pyzipcode


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.db = pyzipcode.ZipCodeDatabase()

    def test_retrieves_zip_code_information(self):
        zip_number = self.db['54115']
        self.assertEquals(zip_number.zip_number, '54115')
        self.assertEquals(zip_number.city, 'De Pere')
        self.assertEquals(zip_number.state, 'WI')

    def test_correct_longitude_value(self):
        zip_number = self.db[54115]
        self.assertTrue(44.42 < zip_number.latitude < 44.44)

    def test_correct_latitude_value(self):
        zip_number = self.db[54115]
        self.assertTrue(-88.08 < zip_number.longitude < -88.06)

    def test_correct_timezone(self):
        zip_number = self.db[54115]
        self.assertEquals(zip_number.timezone, 'America/Chicago')

    def test_radius(self):
        zips = self.db.get_zipcodes_around_radius('54115', 30)
        self.assertTrue('54304' in [z.zip_number for z in zips])

    def test_find_zip_by_city(self):
        zip_number = self.db.find_zip(city='De Pere')[0]
        self.assertEquals('54115', zip_number.zip_number)

    def test_find_zip_by_city_with_multiple_zips(self):
        zips = self.db.find_zip(city='Green Bay')
        self.assertTrue('54302' in [z.zip_number for z in zips])

    def test_find_zips_in_state(self):
        zips = self.db.find_zip(state='WI')
        self.assertTrue('54304' in [z.zip_number for z in zips])
        self.assertTrue('54901' in [z.zip_number for z in zips])


if __name__ == '__main__':
    unittest.main()
