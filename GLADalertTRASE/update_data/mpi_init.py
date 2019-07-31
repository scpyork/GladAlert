#!/usr/bin/env python
'''
http://glad-forest-alert.appspot.com/

115 tiles per date
58cores
29
15


np.where(d[2,:]>1.)


'''

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print (size, rank)

#global imports
import numpy as np
from new_alerts import *
from functions import *
#master imports
if rank == 0:
    import os,tempfile,datetime,sys,time,h5py
    from new_alerts import gettif
#slave imports
else:
    import os
    tempdir = None
    filtered = None


#master setup
if rank == 0:
    print sys.argv
    year = False;

    print 'go'
    #create the directory

    tempdir = tempfile.gettempdir()
    tmpdir = comm.bcast( tempdir,root = 0 )



    now = datetime.datetime.now()
    if not year: year = str(now.year)

    select = sys.argv[1]
    filtered_urls = sys.argv[2].split(',')

    filtered = np.array_split(filtered_urls,size)
    start = time.time()
    print len(filtered),len(filtered_urls)

    print 'mp'


#res = pool.map(download,filtered[:10])


#for i in filtered:
    #res.append( download(i,tempdir) )
else:
    None

comm.barrier()
#send tempdir
tempdir = comm.bcast( tempdir,root = 0 )
# send chunks to everyone
filtered = comm.scatter( filtered,root = 0 )

#print( rank, tempdir, len(filtered))

res = []
for i in filtered:
    res.append( download(i,tempdir) )

filtered = np.concatenate(res,axis=1)

#return newly populates sparse array list
filtered = comm.gather(filtered,root=0)



#print ('.')
comm.barrier()
if rank == 0:
    print ('writing to file (slow)')
    data = np.concatenate(filtered,axis=1)
    data.sort( axis = 1)
    print data[:,:30]
    with h5py.File('data/glad_data_%s.h5'%year,'a') as hf:
        try:      hf.attrs['created_on']
        except:   hf.attrs['created_on'] = str(now)

        if select in hf.keys() : group = hf[select]
        else : group = hf.create_group(select)

        group.attrs['urls'] = ','.join(filtered_urls)
        group.attrs['time'] = time.time() - start

        try: del group['data']
        except: None

        group.create_dataset('data', data.shape , dtype='float32', data = data,compression='gzip',compression_opts=9)


    try: hf.close()
    except: None

    os.system('rm -rf %s/*.tif'%tempdir)
    sys.stdout.flush()
    print( 'finished ')





'''
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
    '''
#hf.close()
