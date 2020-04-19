#################################
##### Name: Yue Ma ##############
##### Uniqname: maamber #########
#################################

import sqlite3

## Create table
conn = sqlite3.connect("Browdway_touring_theater.sqlite")
cur = conn.cursor()

drop_touring_theater = '''
    DROP TABLE IF EXISTS "touring_theater";
'''

create_touring_theater = '''
    CREATE TABLE IF NOT EXISTS "touring_theater" (
        "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Name"  TEXT NOT NULL,
        "City" TEXT NOT NULL,
        "State"  TEXT NOT NULL,
        "Address"    TEXT,
        "Zipcode"    TEXT,
        "Website_link"    TEXT,
        "latitude"    TEXT,
        "longitude"    TEXT
    );
'''

drop_recommended_restaurants = '''
    DROP TABLE IF EXISTS "recommended_restaurants";
'''

create_recommended_restaurants = '''
    CREATE TABLE IF NOT EXISTS "recommended_restaurants" (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'touring_theatre_id' INTEGER,
        'name' TEXT NOT NULL,
        'phone' TEXT,
        'location' TEXT,
        'price' TEXT,
        'rating' REAL,
        'review_count' INTEGER,
        FOREIGN KEY(touring_theatre_id) REFERENCES touring_theater('Id')
    );
'''

drop_show_theater = '''
    DROP TABLE IF EXISTS "show_theater";
'''

create_show_theater = '''
    CREATE TABLE IF NOT EXISTS "show_theater" (
        "touring_show_id"   INTEGER,
        "touring_theater_id"  INTEGER,
        FOREIGN KEY(touring_theater_id) REFERENCES touring_theater('Id'),
        FOREIGN KEY(touring_show_id) REFERENCES touring_show('Id')
    );
'''

drop_touring_show = '''
    DROP TABLE IF EXISTS "touring_show";
'''

create_touring_show = '''
    CREATE TABLE IF NOT EXISTS "touring_show" (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'name' TEXT NOT NULL
    );
'''

cur.execute(drop_touring_theater)
cur.execute(create_touring_theater)

cur.execute(drop_recommended_restaurants)
cur.execute(create_recommended_restaurants)

cur.execute(drop_show_theater)
cur.execute(create_show_theater)

cur.execute(drop_touring_show)
cur.execute(create_touring_show)

conn.commit()
