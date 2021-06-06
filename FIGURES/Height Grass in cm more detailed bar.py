# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:04:08 2021

@author: nashw
"""

import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('postgresql://postgres:thestorm@localhost:5432/TEST1')
df_sql = pd.read_sql_table('data_table',engine)
n=range(1000)
df_sql['ID']= (n)
fig = px.bar(df_sql, x="ID", y="Height Grass_cm", color='site_id', orientation='v',
             hover_data=["site_id", "Technician Name"],
             height=400,
             title='Height of the grass in cm')
fig.show()
pio.renderers.default='browser'
