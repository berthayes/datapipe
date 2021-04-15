#!/usr/local/bin/python3

import mysql.connector
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('luserdb.conf')

my_db_name = cfg.get('userdb', 'database')

mydb = mysql.connector.connect (
    host = cfg.get(my_db_name, 'host'),
    user = cfg.get(my_db_name, 'user'),
    password = cfg.get(my_db_name, 'password'),
)

mycursor = mydb.cursor(buffered=True, raw=False, dictionary=True)

dumb_query = "CREATE DATABASE " + my_db_name
mycursor.execute(dumb_query)


