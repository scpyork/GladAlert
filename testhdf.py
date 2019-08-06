

import json,glob,re,os,h5py,itertools
#import pandas as pd
import numpy as np
from numba import jit
import matplotlib.pyplot as plt

### Input variables

#print __file__
year = 2019

__location__ = './shapefiles'
__files__ = filter(lambda x: 'Global' not in x, 
glob.glob(__location__+'/processed/*.geojson'))
hf= h5py.File('data/glad_data_%s.h5'%year,'r')



date = hf.keys()[0]

data = hf[date]['data']

plt.scatter(x=data[0],y=data[1])
plt.scatter(x=data[0],y=data[1])
plt.show()

hf.close()
