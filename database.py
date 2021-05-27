# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:07:58 2021

@author: Ali
"""



from psycopg2 import connect
import json
import requests
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine


cleanup = (
        'DROP TABLE IF EXISTS system_table CASCADE',
        'DROP TABLE IF EXISTS comments_table',
        'DROP TABLE IF EXISTS data_table'
        )

commands =(
        """
        CREATE TABLE system_table (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255)
            
        )
        """
        ,
        """
        CREATE TABLE comments_table (
            comment_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                title VARCHAR(350) NOT NULL,
                body VARCHAR(500) NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES system_table (user_id)
        )
        """)

sqlCommands = (
        'INSERT INTO system_table (username, password, email) VALUES (%s, %s, %s) RETURNING user_id',
        'INSERT INTO comments_table (title, body, user_id) VALUES (%s, %s, %s)'
        )        
conn = connect("dbname=DBS user=postgres password=uno12345")
cur = conn.cursor()
for command in cleanup :
    cur.execute(command)
for command in commands :
    cur.execute(command)
    print('execute command')
cur.execute(sqlCommands[0], ('mark', 'shf12345','ali.walcot2010@gmail.com'))
userId = cur.fetchone()[0]
cur.execute(sqlCommands[1], ('comment', 'Good job', userId))
cur.execute('SELECT * FROM comments_table')
print(cur.fetchall())

cur.close()
conn.commit()
conn.close()

response = requests.get('https://five.epicollect.net/api/export/entries/DETECT_NR_GROUNDTRUTH2020?per_page=1000')
raw_data = response.text
data   = json.loads(raw_data)
data_df = pd.json_normalize(data['data']['entries'])

data_df['site_id'] = data_df['4_ID_Site']
data_df['longintude'] = pd.to_numeric(data_df['5_Mobile_coordinates.longitude'], errors='coerce')
data_df['latitude'] = pd.to_numeric(data_df['5_Mobile_coordinates.latitude'], errors='coerce')
data_df['Observation_date'] = data_df['1_Date']
data_df['time'] = data_df['2_Time']
data_df['Technician Name'] = data_df['3_Name_Technician']
data_df['Habitat Type'] = data_df['16_Habitat_Type']
data_df['Water Source'] = data_df['18_Water_Source']
data_df['Vegetation Type'] = data_df['25_Vegetation_Type']
data_df['Height Grass_cm'] = data_df['29_Height_Grass_cm']
data_df['Density Grass_cm'] = data_df['30_Density_Grass_cm']
data_df['Moisture content'] = data_df['31_Moisture_content_']
data_df = data_df.loc[:,'site_id':'Moisture content']

engine = create_engine('postgresql://postgres:uno12345@localhost:5432/DBS')
data_df.to_sql('data_table', engine, if_exists = 'replace', index=False)

        


