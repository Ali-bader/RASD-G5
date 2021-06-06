# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 13:20:56 2021

@author: nashw
"""

# Import libraries
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from sqlalchemy import create_engine
import pandas as pd
output_notebook()
#connect the data 
engine = create_engine('postgresql://postgres:uno12345@localhost:5432/DBS')
df_sql = pd.read_sql_table('data_table',engine)
df_sql = df_sql.head(100)
#generate new coulmn
n=range(100)
df_sql['number']= (n)
Index = df_sql['number']
Height = df_sql['Height Grass_cm']
#Calling the figure() function to create the figure of the plot
plot = figure()
#Code to create the barplot
plot.vbar(Index, top = Height, color = "blue", width= 0.1)
#Output the plot
#output_file('C:/Users/nashw/Desktop/barplot.html')
show(plot)
