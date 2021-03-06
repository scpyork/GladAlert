'''
This file is activated through
python -m GLADalertTRASE.update_data


'''
import numpy as np
import os,datetime,sys,h5py
from new_alerts import gettif

args = sys.argv
print(args ,__file__)

__ncores__ = 80
year = 2019

## add to argvs in future
__testRegion__ = '_050W_10S_040W_00N _060W_20S_050W_10S _050W_20S_040W_10S _058W_10S_046W_02N _058W_22S_046W_10S'.split()
__testMonths__ = ['%02d'%int(i) for i in '5'.split()]

now = datetime.datetime.now()
if not year: year = str(now.year)
if not os.path.isdir('./data/'):os.mkdir('./data/')
try:
    with h5py.File('data/glad_data_%s.h5'%year,'r') as hf:
        names = hf.keys()
except:names = []

try: hf.close()
except: None

print (names)



print ('Getting available datasets for the year')


files = gettif(int(year))
daymonths = list(set([i.split('/')[-2] for i in files]))

if __testMonths__:
    daymonths = filter(lambda x: x[:2] in  __testMonths__,  daymonths)

diff = set(daymonths)-set(names)


print ('Running for %s days - 115 tiles each'%len(diff))

for select in diff:
    print select


    filtered_urls = filter(lambda x: select in x, files)

    ## Only download selected tiles.
    if __testRegion__:
        filtered = []
        for r in __testRegion__:
            filtered.extend(filter(lambda x: r in x, filtered_urls))
        filtered_urls = list(set(filtered))



    if len(filtered_urls)<__ncores__:
        __runcores__ = len(filtered_urls)
    else:
        __runcores__ = __ncores__

    if len(filtered_urls)<1:
        print(' No urls to download. ')
        continue
    # urls are fed into the mpi script using cmd arguments.
    links = ','.join(filtered_urls)
    print 'torun' , filtered_urls, __runcores__

    # trigger MPI download process
    os.system('mpirun -np %d python %s %s %s'%(__runcores__,__file__.replace('__main__','mpi_init'),select,links))
