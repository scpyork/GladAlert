
from new_alerts import *
from PIL import Image # $ pip install pillow
from scipy import sparse
import numpy as np
import re

Image.MAX_IMAGE_PIXELS = None

def download(keep,tempdir):
    #print keep
    #class rt:pass
    name = keep.split('/')[-1]
    area = re.findall(r'_(\d+[NESW\b])',name)
    # current file position
    position = map(direction, area)
    group = '|'.join((str(i) for i in position))

    date = keep.split('/')[-2]
    url = keep.replace('gs://','https://storage.cloud.google.com/')#+'?authuser=0'
#2

    ##  copy /  download the files into the temp directory
    (os.popen('gsutil cp %s %s/%s >/dev/null 2>&1 && echo "Copied: %s" >> temp.log'%(keep,tempdir,name,keep))) #.read())
    ## Read image pixels using pillow library
    im = Image.open('%s/%s'%(tempdir,name))
    ## Image pixels to a sparse array
    data = sparse.coo_matrix(im,int)
    ## remove downloaded file
    os.system('rm %s/%s'%(tempdir,name))


    data = np.array([
        data.row.astype(float)* 0.00025 + position[0] ,
        #/float(data.shape[0])*(float(position[2]-position[0]))+position[0],
        data.col.astype(float)* 0.00025 + position[1] ,
        #/float(data.shape[1])*(float(position[3]-position[1]))+position[1],
        data.data
    ])

    #print data[:,0],data[:,-1], position

    return data
