# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 13:53:59 2021

@author: Mohammed
"""


#from bokeh.plotting import figure, show, output_file


import rasterio
from matplotlib import pyplot
from rasterio.plot import show


src = rasterio.open("C:/Users/Mohammed/Desktop/S2B_MSIL1C_20200922T142739_N0209_R053_T21NTE_20200922T162102.SAFE/GRANULE/L1C_T21NTE_A018526_20200922T142733/IMG_DATA/T21NTE_20200922T142739_B08.jp2")
pyplot.imshow(src.read(1), cmap='pink')
#matplotlib.image.AxesImage object at 0x...===
pyplot.show()

#Contour===============
fig, ax = pyplot.subplots(1, figsize=(12, 12))
show((src, 1), cmap='Greys_r', interpolation='none', ax=ax)
#<matplotlib.axes._subplots.AxesSubplot object at 0x...
show((src, 1), contour=True, ax=ax)
#matplotlib.axes._subplots.AxesSubplot object at 0x...>
pyplot.show()