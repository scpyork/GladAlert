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
import os
import numpy as np
from new_alerts import *
from functions import *
#master imports
if rank == 0:
    import tempfile,datetime,sys,time,h5py
    from new_alerts import gettif
#slave imports
else:
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

    #we need a row preserving sort
    data = data[np.argsort(data[:,1])]
    data = data[np.argsort(data[:,0])]

    #test the sorting problem
    '''
    import pandas as pd
    pd.DataFrame(data).to_csv('test.csv')
    print 'csv'
    '''

    '''
    f = tuple(open('test.csv'))
    plt.scatter(np.array(f[1].split(',')).astype(float),np.array(f[2].split(',')).astype(float))
    '''

    print max(data[0,:]), max(data[1,:]), max(data[2,:]),'\n', min(data[0,:]), min(data[1,:]),'\n',data[:,::50]

    with h5py.File('data/glad_data_%s.h5'%year,'a') as hf:
        try:      hf.attrs['created_on']
        except:   hf.attrs['created_on'] = str(now)

        if select in hf.keys() : group = hf[select]
        else : group = hf.create_group(select)

        group.attrs['urls'] = ','.join(filtered_urls)
        group.attrs['time'] = time.time() - start

        try: del group['data']
        except: None

        group.create_dataset('data', data.shape , data = data,dtype=float,compression='gzip',compression_opts=9)


    try: hf.close()
    except: None

    os.system('rm -rf %s/*.tif'%tempdir)
    sys.stdout.flush()
    print( 'finished ')
