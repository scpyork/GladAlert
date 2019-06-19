#!/usr/bin/env python
from new_alerts import *

import numpy as np
import re,os
from PIL import Image # $ pip install pillow
Image.MAX_IMAGE_PIXELS = None


def direction(d):
    if d[-1] in ['W','S']:
          return -int(d[:-1])
    else: return int(d[:-1])


keep = files[0]
name = keep.split('/')[-1]
area = re.findall(r'_(\d+[NESW\b])',name)
position = map(direction, area)

url = keep.replace('gs://','https://storage.cloud.google.com/')#+'?authuser=0'

print os.popen('gsutil cp %s ./%s'%(keep,name)).read()





im = np.array(Image.open(name)) #NOTE: it requires pillow 2.8+
