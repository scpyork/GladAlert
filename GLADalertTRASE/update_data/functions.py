
from .new_alerts import *
import numpy as np
import re,os,h5py,tempfile,datetime,gc,sys
from PIL import Image # $ pip install pillow
from scipy import sparse

Image.MAX_IMAGE_PIXELS = None

def download(keep):
    print keep

    class rt:pass
    name = keep.split('/')[-1]
    area = re.findall(r'_(\d+[NESW\b])',name)
    # current file position
    position = map(direction, area)
    group = '|'.join((str(i) for i in position))

    rt.position = position
    rt.group = group

    date = keep.split('/')[-2]
    url = keep.replace('gs://','https://storage.cloud.google.com/')#+'?authuser=0'
#2
    rt.date = date
    rt.url = url

    print (os.popen('gsutil cp %s %s/%s'%(keep,tempdir,name)).read())

    im = Image.open('%s/%s'%(tempdir,name))
    data = np.array(im,int)
    os.system('rm %s/*.tif'%tempdir)

    err = 0
    while len(data.shape) == 0:
        gc.collect();
        im = Image.open('%s/%s'%(tempdir,name))
        data = sparse.coo_matrix(im)
        print ('memory issues - ',name)

        err+= 1
        if err > 20:
            hf.close()
            sys.exit('failing to open image')

    rt.data = np.array([data.row,data.col,data.data],float)

    return rt
