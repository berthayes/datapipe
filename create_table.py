#!/usr/local/bin/python3

import mysql.connector
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('luserdb.conf')

my_db_name = 'userdb'

mydb = mysql.connector.connect (
    host = cfg.get(my_db_name, 'host'),
    user = cfg.get(my_db_name, 'user'),
    password = cfg.get(my_db_name, 'password'),
    database = cfg.get(my_db_name, 'database')
)

mycursor = mydb.cursor(buffered=True, raw=False, dictionary=True)

create_table_query = "CREATE TABLE lusers ( \
 id INT AUTO_INCREMENT PRIMARY KEY, \
 Number INT, \
 Gender VARCHAR(10), \
 Nameset VARCHAR(20), \
 Title VARCHAR(5), \
 GivenName VARCHAR(25), \
 MiddleInitial VARCHAR(1), \
 Surname VARCHAR(25), \
 StreetAddress VARCHAR(255), \
 City VARCHAR(255), \
 State VARCHAR(2), \
 StateFull VARCHAR(50), \
 ZipCode INT, \
 Country VARCHAR(2), \
 CountryFull VARCHAR(50), \
 EmailAddress VARCHAR(255), \
 Username VARCHAR(255), \
 Password VARCHAR(255), \
 BrowserUserAgent VARCHAR(255), \
 TelephoneNumber VARCHAR(15), \
 TelephoneCountryCode TINYINT, \
 MothersMaiden VARCHAR(25), \
 Birthday VARCHAR(25), \
 Age TINYINT, \
 TropicalZodiac VARCHAR(55), \
 CCType VARCHAR(25), \
 CCNumber BIGINT, \
 CVV2 SMALLINT, \
 CCExpires VARCHAR(25), \
 NationalID VARCHAR(25), \
 UPS VARCHAR(55), \
 WesternUnionMTCN VARCHAR(55), \
 MoneyGramMTCN VARCHAR(55), \
 Color VARCHAR(25), \
 Occupation VARCHAR(255), \
 Company VARCHAR(255), \
 Vehicle VARCHAR(55), \
 Domain VARCHAR(255), \
 BloodType VARCHAR(5), \
 Pounds DECIMAL(5,2), \
 Kilograms DECIMAL(5,2), \
 FeetInches VARCHAR(255), \
 Centimeters INT, \
 GUID VARCHAR(255), \
 Latitude VARCHAR(255), \
 Longitude VARCHAR(255))"

mycursor.execute(create_table_query)
