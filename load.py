import csv
from pony.orm import commit, db_session
from pyzipcode import ZipCodeModel


@db_session
def load_data(file_name):
    for zn, city, state, tz, lat, lng, country in csv.reader(open(file_name, 'r')):
        if zn and city and state and country:
            z = ZipCodeModel(
                zip_number=zn,
                city=city,
                state=state,
                country=country,
                latitude=lat,
                longitude=lng,
                timezone=tz
            )
            print 'Creating [{z.zip_number}] {z.city} {z.state} {z.country}'.format(z=z)
    commit()


if __name__ == '__main__':
    load_data('zip_code_database.csv')
