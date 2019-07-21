#!/usr/bin/env python
'''
http://glad-forest-alert.appspot.com/

File hierarchy:

latlon (minx|maxx|miny|maxy)
    -> year (yyyy)
        -> dataset (pixelmat)
           ->> dataset attrs


'''

year = False;

from .new_alerts import *
import numpy as np
import re,os,h5py,tempfile,datetime,gc,sys
from PIL import Image # $ pip install pillow
Image.MAX_IMAGE_PIXELS = None


from pathos.multiprocessing import ProcessPool
from .functions import *
pool = ProcessPool(nodes=25)

print 'go'
#create the directoryn
if not os.path.isdir('./data/'):os.mkdir('./data/')
tempdir = tempfile.gettempdir()


now = datetime.datetime.now()
if not year: year = str(now.year)

## Create the wrapper hdf5 file
with h5py.File('glad_data.h5','a') as hf:
    try:      hf.attrs['created_on']
    except:   hf.attrs['created_on'] = str(now)
    latlon = hf.keys()
    print '.'
    files = getdates(int(year),par=True)
    print ('starting')


    files_year = filter(lambda x: re.match(r'.*/alert'+year[-2:]+'_',x), files)

    daymonths = list(set([i.split('/')[-2] for i in files_year]))


    select = daymonths[0]

    filtered = filter(lambda x: select in x, files_year)
    print len(filtered)

    print 'mp'


    for rt in pool.map(download,filtered):
    # filter out just the latest year, the previous exists in a separate directory


        ## create test cascade
        if group in latlon : group = hf[rt.group]
        else :
            latlon.append(rt.group)
            group = hf.create_group(rt.group)
            # add this on such that we dont get problems when moving on to new countries or years...

        #year
        if year in group.keys():g_year = group[year]
        else:g_year = group.create_group(year)


        # dont write again
        if rt.date in g_year.keys(): continue

        dset = g_year.create_dataset(rt.date, rt.data.shape , dtype='int8', data = rt.data,compression='gzip',compression_opts=9)

        position = rt.position
        dset.attrs['min_x']= position[0]
        dset.attrs['min_y']= position[1]
        dset.attrs['max_x']= position[2]
        dset.attrs['max_y']= position[3]

        dset.attrs['url']=rt.url
        dset.attrs['shape']= rt.data.shape
        group.attrs['shape']= rt.data.shape


        print(group,date)

    hf.attrs['last_modified'] = str(datetime.datetime.now())
#hf.close()
os.system('rm -rf %s/*.tif'%tempdir)
print( 'finished ')