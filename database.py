#################################
##### Name: Yue Ma ##############
##### Uniqname: maamber #########
#################################

import sqlite3
import json
import csv

def create_db():
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


def load_theaters():
    with open('data/theater_info.json') as f:
        data = json.load(f)

    insert_Theaters='''
            INSERT INTO touring_theater
            VALUES (NULL,?,?,?,?,?,?,?,?)
            '''
    conn = sqlite3.connect("Browdway_touring_theater.sqlite")
    cur = conn.cursor()
    for record in data:
        record_value= [record['name'],record['city'],record['state'],record['address'],record['zipcode'],record['website'],record['latitude'],record['longitude']]
        cur.execute(insert_Theaters,record_value)
    conn.commit()
    conn.close()

def load_shows():   
    with open('data/musical_info.json') as f:
        data = json.load(f)
    insert_Shows='''
            INSERT INTO touring_show
            VALUES (NULL,?)
            '''
    conn = sqlite3.connect("Browdway_touring_theater.sqlite")
    cur = conn.cursor()
    for record in data:
        cur.execute(insert_Shows,[record])
    conn.commit()
    conn.close()

def load_restaurants():
    with open('data/restaurant_info.json') as f:
        data = json.load(f)

    select_theater_id_sql='''
        SELECT Id FROM touring_theater WHERE Name= ?
        '''
    insert_restaurant_sql='''
        INSERT INTO recommended_restaurants
        VALUES (NULL,?,?,?,?,?,?,?)
        '''
    conn = sqlite3.connect('Browdway_touring_theater.sqlite')
    cur = conn.cursor()
    for record in data:
        # get id for theater
        cur.execute(select_theater_id_sql,[record['theater']])
        res=cur.fetchone()
        touring_theatre_id=None
        if res is not None:
            touring_theatre_id=res[0]  
        # insert value into table
        record_value= [touring_theatre_id,record['name'],record['phone'],record['location'],record['price'],record['raing'],record['review_count']]
        cur.execute(insert_restaurant_sql,record_value)
    conn.commit()
    conn.close()

def load_show_theater():
    file_contents=open('data/show_theater.csv','r')
    file_reader=csv.reader(file_contents)
    next(file_reader) # skip header row

    insert_show_theater_sql='''
        INSERT INTO show_theater
        VALUES (?,?)
        '''
    conn = sqlite3.connect('Browdway_touring_theater.sqlite')
    cur = conn.cursor()
    for row in file_reader:
        #print(row)
        record_value=[row[0],row[1]]
        cur.execute(insert_show_theater_sql,record_value)
    conn.commit()
    conn.close()

create_db()
load_theaters()
load_shows()
load_restaurants()
load_show_theater()

