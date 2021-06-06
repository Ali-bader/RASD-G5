# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:28:48 2021

@author: nashw
"""

import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine
import pandas as pd
#connect the data
engine = create_engine('postgresql://postgres:thestorm@localhost:5432/TEST1')
df_sql = pd.read_sql_table('data_table',engine)
#create new coulmn
n=range(1000)
df_sql['ID']= (n)

fig = px.line(df_sql, x="ID", y="Height Grass_cm", title='Height Grass_cm')
fig.show()
pio.renderers.default='browser'
