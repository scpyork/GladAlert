'''
Test plot a 1000x1000 reduced version of the tiles presented.
'''

import sys
import re
import matplotlib.pyplot as plt
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from scipy import sparse


def direction(d):
    '''Determine the grid cells numerical latlon'''
    if d[-1] in ['W','S']:return -int(d[:-1])
    else: return int(d[:-1])


def draw(f, show = False):
     '''
     show - plot using imagemagick or the like
     editing required. (make negative and exagerate)
     '''
     im = Image.open(f)
     im = im.resize((1000,1000), resample=Image.BILINEAR)
     if show: im.show()
     data = sparse.coo_matrix(im,int)
     name = f.split('/')[-1]
     area = re.findall(r'_(\d+[NESW\b])',name)
     # current file position
     position = map(direction, area)

     plt.scatter(data.row.astype(float)* 0.00025 +
    float(position[0]),data.col.astype(float)* 0.00025 + float(position[1]),c=data.data, alpha = .5,s=data.data**3)
     plt.title(f)
     plt.show()
