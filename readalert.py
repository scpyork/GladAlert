

###############

###OBSOLETE


################







#!/usr/bin/env python
'''
http://glad-forest-alert.appspot.com/

File hierarchy:

latlon (minx|maxx|miny|maxy)
    -> year (yyyy)
        -> dataset (pixelmat)
           ->> dataset attrs


'''



from new_alerts import *
import numpy as np
import re,os,h5py,tempfile
from PIL import Image # $ pip install pillow
Image.MAX_IMAGE_PIXELS = None

#create the directory
if not os.path.isdir('./data/'):os.mkdir('./data/')
tempdir = tempfile.gettempdir()

## Create the wrapper hdf5 file
hf = h5py.File('glad_data.h5')
try:      hf.attrs['created_on']
except:   hf.attrs['created_on'] = str(datetime.datetime.now())
latlon = hf.keys()
year = str(year)






files = getdates(year)

a = filter(lambda x: re.match(r'.*/alert'+year[-2:]+'_',x), files)
fdsafds = fdsfds

for keep in filter(lambda x: re.match(r'.*/alert'+year[-2:]+'_',x), files):
# filter out just the latest year, the previous exists in a separate directory
    name = keep.split('/')[-1]
    area = re.findall(r'_(\d+[NESW\b])',name)
    # current file position
    position = map(direction, area)
    group = '|'.join((str(i) for i in position))

    ## create test cascade
    #latlon
    if group in latlon : group = hf[group]
    else : group = hf.create_group(group)

    #year
    if year in group.keys():g_year = group[year]
    else:g_year = group.create_group(year)

    date = keep.split('/')[-2]
    url = keep.replace('gs://','https://storage.cloud.google.com/')#+'?authuser=0'

    temp = tempfile.TemporaryFile() #2
    print (os.popen('gsutil cp %s %s/%s'%(keep,tempdir,name)).read())

    im = Image.open('%s/%s'%(tempdir,name))
    data = np.array(im) #NOTE: it requires pillow 2.8+


    dset = group.create_dataset(date, im.size , dtype='int8', data = data,compression='gzip',compression_opts=9)

    dset.attrs['min_x']= position[0]
    dset.attrs['min_y']= position[1]
    dset.attrs['max_x']= position[2]
    dset.attrs['max_y']= position[3]

    dset.attrs['url']=url
    dset.attrs['shape']= im.size


    print(group,date)

hf.attrs['last_modified'] = str(datetime.datetime.now())
hf.close()
os.system('rm -rf %s/*.tif'%tempdir)
print( 'finished ')
