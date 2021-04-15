import csv
import time
from collections import namedtuple
import mysql.connector
from configparser import ConfigParser
import argparse
import sys
#import daemonize

parser = argparse.ArgumentParser(description=
                                 '''
                                Feed a MySQL database lines from a CSV file
                                ''')
parser.add_argument('-f', dest='csv_file', action='store', help='the full path of the .csv file to read')
parser.add_argument('-t', dest='time_delay', action='store', default=0, help='number of seconds to wait between loading records')
parser.add_argument('-d', dest='daemonize', action='store_true', help='run script as a deamon')



args = parser.parse_args()
time_delay = int(args.time_delay)


if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

cfg = ConfigParser()
cfg.read('luserdb.conf')

my_db_name = cfg.get('userdb', 'database')

mydb = mysql.connector.connect(
    host=cfg.get(my_db_name, 'host'),
    user=cfg.get(my_db_name, 'user'),
    password=cfg.get(my_db_name, 'password'),
    database=cfg.get(my_db_name, 'database'),
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor(buffered=True, raw=False, dictionary=True)

# csv_file = cfg.get(my_db_name, 'input_file')
csv_file = args.csv_file


#if args.daemonize:
#    daemonize.daemonize('/tmp/db_insert_daemon.pid',
#                stdin='/dev/null',
#                stdout='/tmp/db_insert_daemon.log',
#                stderr='/tmp/db_insert_daemon.log')

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)

    for r in f_csv:
        row = Row(*r)
        insert_query = "INSERT INTO lusers ( \
            Number, \
            Gender, \
            NameSet, \
            Title, \
            GivenName, \
            MiddleInitial, \
            Surname, \
            StreetAddress, \
            City, \
            State, \
            StateFull, \
            ZipCode, \
            Country, \
            CountryFull, \
            EmailAddress, \
            Username, \
            Password, \
            BrowserUserAgent, \
            TelephoneNumber, \
            TelephoneCountryCode, \
            MothersMaiden, \
            Birthday, \
            Age, \
            TropicalZodiac, \
            CCType, \
            CCNumber, \
            CVV2, \
            CCExpires, \
            NationalID, \
            UPS, \
            WesternUnionMTCN, \
            MoneyGramMTCN, \
            Color, \
            Occupation, \
            Company, \
            Vehicle, \
            Domain, \
            BloodType, \
            Pounds, \
            Kilograms, \
            FeetInches, \
            Centimeters, \
            GUID, \
            Latitude, \
            Longitude \
            ) VALUES ( \
            %(Number)s, \
            %(Gender)s, \
            %(NameSet)s, \
            %(Title)s, \
            %(GivenName)s, \
            %(MiddleInitial)s, \
            %(Surname)s, \
            %(StreetAddress)s, \
            %(City)s, \
            %(State)s, \
            %(StateFull)s, \
            %(ZipCode)s, \
            %(Country)s, \
            %(CountryFull)s, \
            %(EmailAddress)s, \
            %(Username)s, \
            %(Password)s, \
            %(BrowserUserAgent)s, \
            %(TelephoneNumber)s, \
            %(TelephoneCountryCode)s, \
            %(MothersMaiden)s, \
            %(Birthday)s, \
            %(Age)s, \
            %(TropicalZodiac)s, \
            %(CCType)s, \
            %(CCNumber)s, \
            %(CVV2)s, \
            %(CCExpires)s, \
            %(NationalID)s, \
            %(UPS)s, \
            %(WesternUnionMTCN)s, \
            %(MoneyGramMTCN)s, \
            %(Color)s, \
            %(Occupation)s, \
            %(Company)s, \
            %(Vehicle)s, \
            %(Domain)s, \
            %(BloodType)s, \
            %(Pounds)s, \
            %(Kilograms)s, \
            %(FeetInches)s, \
            %(Centimeters)s, \
            %(GUID)s, \
            %(Latitude)s, \
            %(Longitude)s)"

        # user_info = dict()
        user_info = {
            'Number': row.Number,
            'Gender': row.Gender,
            'NameSet': row.NameSet,
            'Title': row.Title,
            'GivenName': row.GivenName,
            'MiddleInitial': row.MiddleInitial,
            'Surname': row.Surname,
            'StreetAddress': row.StreetAddress,
            'City': row.City,
            'State': row.State,
            'StateFull': row.StateFull,
            'ZipCode': row.ZipCode,
            'Country': row.Country,
            'CountryFull': row.CountryFull,
            'EmailAddress': row.EmailAddress,
            'Username': row.Username,
            'Password': row.Password,
            'BrowserUserAgent': str(row.BrowserUserAgent),
            'TelephoneNumber': row.TelephoneNumber,
            'TelephoneCountryCode': row.TelephoneCountryCode,
            'MothersMaiden': row.MothersMaiden,
            'Birthday': row.Birthday,
            'Age': row.Age,
            'TropicalZodiac': row.TropicalZodiac,
            'CCType': row.CCType,
            'CCNumber': row.CCNumber,
            'CVV2': row.CVV2,
            'CCExpires': row.CCExpires,
            'NationalID': row.NationalID,
            'UPS': row.UPS,
            'WesternUnionMTCN': row.WesternUnionMTCN,
            'MoneyGramMTCN': row.MoneyGramMTCN,
            'Color': row.Color,
            'Occupation': row.Occupation,
            'Company': row.Company,
            'Vehicle': row.Vehicle,
            'Domain': row.Domain,
            'BloodType': row.BloodType,
            'Pounds': row.Pounds,
            'Kilograms': row.Kilograms,
            'FeetInches': row.FeetInches,
            'Centimeters': row.Centimeters,
            'GUID': row.GUID,
            'Latitude': row.Latitude,
            'Longitude': row.Longitude
        }

        mycursor.execute(insert_query, user_info)
        if time_delay > 0:
            mydb.commit()
            time.sleep(time_delay)


mydb.commit()
mycursor.close()
mydb.close()
