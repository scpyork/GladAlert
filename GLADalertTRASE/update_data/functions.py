
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

    #rt.position = position
    #rt.group = group

    date = keep.split('/')[-2]
    url = keep.replace('gs://','https://storage.cloud.google.com/')#+'?authuser=0'
#2
    #rt.date = date
    #rt.url = url
    #this was a print
    (os.popen('gsutil cp %s %s/%s >/dev/null 2>&1 && echo "Copied: %s" >> temp.log'%(keep,tempdir,name,keep)))#.read())

    im = Image.open('%s/%s'%(tempdir,name))
    data = sparse.coo_matrix(im,int)
    os.system('rm %s/%s'%(tempdir,name))

    err = 0
    '''
    while len(data.shape) == 0:
        gc.collect();
        im = Image.open('%s/%s'%(tempdir,name))
        data = sparse.coo_matrix(im)
        print ('memory issues - ',name)

        err+= 1
        if err > 20:
            hf.close()
            sys.exit('failing to open image')
    '''
    data = np.array([
        data.row.astype(float)/float(data.shape[0])*(float(position[2]-position[0]))+position[0],
        data.col.astype(float)/float(data.shape[1])*(float(position[3]-position[1]))+position[1],
        data.data
    ])

    #rt.data = data

    return data
