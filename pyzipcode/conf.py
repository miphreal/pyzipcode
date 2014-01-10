import os


db_settings = dict(
    # Full path to db
    db_location=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zipcodes.sqlite'),
    db_engine='sqlite',
    debug=False
)
