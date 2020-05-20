#!/usr/bin/env python

import os
import pandas as pd
from sqlalchemy import create_engine

# Set database variables
db_user = 'weatherlogger'
db_pass = 'weatherpass'
db_host = 'localhost'
db_name = 'weatherdb'

# Read in the new data
df = pd.read_csv('/home/william/Scripts/Weather/weather_log.csv',
                 usecols=['time', 'temperature_C', 'humidity', 'wind_max_m_s',
                          'wind_avg_m_s', 'wind_dir_deg', 'rain_mm'],
                 parse_dates=[0], index_col=0)

# Resample the data into 10 minute blocks
df = df.resample('10Min').mean()

# Create database engine
engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(
    db_user, db_pass, db_host, db_name)

# Append data to database table called weather
try:
    df.to_sql('weather', engine, if_exists='append')
except Exception as e:
    print(e)

# Delete csv file
try:
    os.remove('/home/william/Scripts/Weather/weather_log.csv')
except OSError as e:
    print('Error: {} - {}.'.format(e.filename, e.strerror))
